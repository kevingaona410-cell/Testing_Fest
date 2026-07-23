"""Módulo del servidor de chat.

Proporciona la clase Server con configuración inyectable y lógica separada
para parsear buffers de mensajes.
"""

import socket
import threading


def parse_buffer(buffer: str):
    """Parsea mensajes terminados en '\n' y devuelve mensajes completos y residuo."""
    messages = []
    while '\n' in buffer:
        msg_line, buffer = buffer.split('\n', 1)
        if msg_line.strip():
            messages.append(msg_line)
    return messages, buffer


class Server:
    # Configuración Inicial
    def __init__(self, ip: str = '127.0.0.1', port: int = 8080):
        # Crear socket TCP/IP
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.clients = []  # Lista para almacenar conexiones de clientes activos
        self.lock = threading.Lock()

    def broad(self, message, origin=None):
        """Difunde un mensaje a todos los clientes excepto al remitente (origin)"""
        disconnect = []
        with self.lock:
            clients_copy = list(self.clients)
        for client in clients_copy:
            if client != origin:
                try:
                    client.send((message + '\n').encode('utf-8'))
                except (socket.error, ConnectionResetError, OSError):
                    disconnect.append(client)
        
        # Eliminar y cerrar conexiones fallidas 
        for disc_client in disconnect:
            with self.lock:
                if disc_client in self.clients:
                    self.clients.remove(disc_client)
            try:
                disc_client.close()
            except OSError:
                pass


    
    def send_message(self, client, name):
        """Recibe mensajes del cliente y los retransmite a otros"""
        buffer = ''
        while True:
            try:
                # Recibir hasta 1024 bytes del cliente
                message = client.recv(1024).decode('utf-8')

                # Si el cliente se desconecta, recv() retorna b'', detener el hilo
                if not message:
                    break

                # Acumular datos en buffer y procesar mensajes completos (terminan en \n)
                buffer += message
                messages, buffer = parse_buffer(buffer)
                for msg_line in messages:
                    print(f'[{name}] {msg_line}')
                    self.broad(f'[{name}] {msg_line}', origin=client)
            except (socket.error, ConnectionResetError, OSError):
                break

    def close_server(self):
        """Cierra el servidor y desconecta todos los clientes"""
        print('Warning: Closing server.')
        self.broad('Server is closing.')

        with self.lock:
            for client in list(self.clients):
                try:
                    client.close()
                except OSError:
                    pass
            self.clients.clear()
        try:
            self.server.close()
        except OSError:
            pass
        print('Server closed.')

    # Hilo del cliente en el servidor
    def handle_client(self, client_conn, client_addr):
        """Maneja la conexión de un cliente en un hilo separado"""
        name = None  
        try:
            name = client_conn.recv(1024).decode('utf-8').strip()
            
            # Agregar cliente de forma segura
            with self.lock:
                self.clients.append(client_conn)
            print(f'{name} se ha conectado desde {client_addr}.')
            
            self.broad(f'{name} has joined the chat.', origin=client_conn)
            self.send_message(client=client_conn, name=name)
        except (socket.error, ConnectionResetError, OSError) as e:
            print(f'Error handling client {client_addr}: {e}')
        finally:
            with self.lock:
                if client_conn in self.clients:
                    self.clients.remove(client_conn)
            try:
                client_conn.close()
            except OSError:
                pass
            if name:
                print(f'{name} has disconnected.')
                self.broad(f'{name} has left the chat.')
            else:
                print(f'Client {client_addr} disconnected before sending username.')
    # Inicialización del Servidor
    def init_server(self):
        """Inicia el servidor y acepta conexiones de clientes"""
        try:
            self.server.bind((self.ip, self.port))
            self.port = self.server.getsockname()[1]
            self.server.listen()
            print(f'Server initialized on {self.ip}:{self.port}.')

            while True: 
                # Aceptar nueva conexión de cliente
                client_conn, client_addr = self.server.accept()
                # Crear un hilo para manejar al cliente de forma concurrente
                thread = threading.Thread(target=self.handle_client, args=(client_conn, client_addr))
                thread.daemon = True  # Hacer que el hilo termine cuando el programa termina
                thread.start()
        except KeyboardInterrupt:
            # Ctrl+C para cerrar el servidor
            self.close_server()

# Instanciar y ejecutar el servidor
if __name__ == '__main__':
    server = Server()
    server.init_server()
