# Importacion de librerias
import socket
import threading

def is_valid_message(message: str) -> bool:
    return bool(message and message.strip())

# Clase Cliente
class Client:    
    # Configuracion del cliente
    def __init__(self, ip: str = '127.0.0.1', port: int = 8080):
        self.server_ip = ip
        self.server_port = port
        self.client = None  
    # Intenta conectar al servidor
    def connect_to_server(self, name, max_retries=None):
        """Conecta al servidor y envía el nombre del usuario"""
        attempts = 0
        while max_retries is None or attempts <= max_retries:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                self.client.connect((self.server_ip, self.server_port))
                # Enviar nombre al servidor
                self.client.send((name + '\n').encode('utf-8'))
                print(f'Connected to server as {name}.')
                return self.client
            except (socket.error, ConnectionResetError, OSError):
                attempts += 1
                if max_retries is not None and attempts > max_retries:
                    raise
                print('Error connecting to server. Retrying...')

    # Recibir mensaje
    def receive_message(self, socket_client):
        """Hilo para recibir mensajes del servidor continuamente"""
        while True:
            try:
                message = socket_client.recv(1024)

                if not message:
                    print('Server disconnected.')
                    socket_client.close()
                    return
                
                # Decodificar y mostrar mensaje recibido
                print(f'\n{message.decode("utf-8")}', end='')

            except (socket.error, ConnectionResetError, OSError):
                print('Error: Lost connection with server.')
                socket_client.close()
                return

    # Enviar mensaje
    def send_message(self, socket_client):
        try:
            message = input('Enter a message: ')
            if is_valid_message(message):
                socket_client.send((message + '\n').encode('utf-8'))
            else:
                print('Message cannot be empty.')
        except (socket.error, ConnectionResetError, OSError):
            print('Error sending message.')

    # Inicia el cliente
    def init_client(self):
        name = input('Enter your name: ')

        # Conectar al servidor
        socket_client = self.connect_to_server(name)
    
        try:
            # Crear hilo para recibir mensajes (daemon para terminar con el programa)
            hear_thread = threading.Thread(target=self.receive_message, args=(socket_client,), daemon=True)
            hear_thread.start()

            # Bucle principal para enviar mensajes
            while True:
                self.send_message(socket_client)

        except KeyboardInterrupt:
            # Ctrl+C para desconectar
            print('\nDisconnecting...')
            socket_client.close()
        except (socket.error, ConnectionResetError, OSError) as e:
            print(f'Error: {e}')
            socket_client.close()

# Instanciar y ejecutar el cliente
if __name__ == '__main__':
    client = Client()
    client.init_client()