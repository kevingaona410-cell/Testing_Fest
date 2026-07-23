import sys
import os
import time
import threading
from pathlib import Path

# Agregar la carpeta 'source' a sys.path 
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from source.server import Server
from source.client import Client

DIRECCION_IP = '127.0.0.1'

# FUNCIONES AUXILIARES PARA LAS PRUEBAS
def create_test_server():
    """Crea e inicia el servidor en un puerto dinámico (0) dentro de un hilo secundario."""
    server_obj = Server(ip=DIRECCION_IP, port=0)
    
    # Iniciar el bucle del servidor en un hilo daemon para que finalice cuando terminen los tests
    server_thread = threading.Thread(target=server_obj.init_server, daemon=True)
    server_thread.start()
    
    # Pausa breve para permitir que el socket complete el bind
    time.sleep(0.1)
    return server_obj


def connect_test_client(username, port):
    """Crea una instancia de Client y la conecta al servidor de prueba en ejecucion."""
    client_obj = Client(ip=DIRECCION_IP, port=port)
    client_socket = client_obj.connect_to_server(username, max_retries=1)
    time.sleep(0.1)
    return client_socket


# PRUEBAS DE INTEGRACIÓN 

def test_multiple_clients_can_connect():
    """ VERIFICA QUE MÚLTIPLES CLIENTES PUEDAN CONECTARSE AL SERVIDOR SIMULTÁNEAMENTE."""
    server = create_test_server()
    port = server.port  # Obtener el puerto asignado dinámicamente

    client_one = None
    client_two = None

    try:
        client_one = connect_test_client("Sarah", port)
        client_two = connect_test_client("David", port)

        assert len(server.clients) == 2

    finally:
        if client_one:
            client_one.close()
        if client_two:
            client_two.close()
        server.close_server()


def test_broadcast_message_reaches_all_clients():
    """ VERIFICA EL BROADCAST: UN MENSAJE ENVIADO POR UN CLIENTE ES RECIBIDO POR LOS DEMÁS."""
    server = create_test_server()
    port = server.port

    client_one = None
    client_two = None
    client_three = None

    try:
        # ARRANGE: Conectar tres clientes
        client_one = connect_test_client("Sarah", port)
        client_two = connect_test_client("David", port)
        client_three = connect_test_client("Elena", port)

        client_one.settimeout(2)
        client_two.settimeout(2)
        client_three.settimeout(2)

        client_two.recv(1024)

        # ACT: Sarah envía un mensaje al grupo
        test_message = "Hello everyone\n"
        client_one.send(test_message.encode('utf-8'))
        time.sleep(0.2)

        # David y Elena leen el mensaje retransmitido por Sarah
        response_two = client_two.recv(1024).decode('utf-8')
        response_three = client_three.recv(1024).decode('utf-8')

        # ASSERT: Verificar que ambos clientes recibieron el mensaje formateado
        assert "[Sarah] Hello everyone" in response_two
        assert "[Sarah] Hello everyone" in response_three

    finally:
        if client_one:
            client_one.close()
        if client_two:
            client_two.close()
        if client_three:
            client_three.close()
        server.close_server()

def test_abrupt_disconnection_does_not_crash_server():
    """ RESILIENCIA: LA DESCONEXIÓN INESPERADA DE UN CLIENTE NO AFECTA A LOS DEMÁS."""
    server = create_test_server()
    port = server.port

    client_one = None
    client_two = None
    client_three = None

    try:
        # ARRANGE: Conectar tres clientes
        client_one = connect_test_client("Sarah", port)
        client_two = connect_test_client("David", port)
        client_three = connect_test_client("Elena", port)

        client_one.settimeout(2)
        client_two.settimeout(2)
        client_three.settimeout(2)

        # ACT: Simular desconexión abrupta cerrando el socket de David directamente
        client_two.close()
        client_two = None
        time.sleep(0.3)

        # ASSERT 1: El servidor remueve a David y mantiene a los clientes activos restantes
        assert len(server.clients) == 2

        # ACT 2: Sarah envía un mensaje para confirmar que el chat sigue funcionando
        client_one.send(b"Still connected\n")
        time.sleep(0.2)

        response_three = client_three.recv(1024).decode('utf-8')

        # ASSERT 2: Elena recibe correctamente el mensaje de Sarah
        assert "[Sarah] Still connected" in response_three

    finally:
        if client_one:
            client_one.close()
        if client_two:
            client_two.close()
        if client_three:
            client_three.close()
        server.close_server()