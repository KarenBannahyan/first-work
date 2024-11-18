import threading
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime
from ClientSocket import ClientSocket


class SocketServer:

    def __init__(self, host, port):
        self.ipAddress = host
        self.messagingServer = socket(AF_INET, SOCK_STREAM)
        self.messagingServer.bind((host, port))
        self.messagingServer.listen()

        self.clients = []
        self.clientSocket = ClientSocket(host, port, True)
        self.startLoop()

    def broadcastMessage(self, message, client_address):
        # Записываем сообщение в лог
        self.logMessage(message, client_address)

        # Отправляем сообщение всем подключенным клиентам
        for client in self.clients:
            try:
                client.send(message)
            except:
                # Если клиент отключился, удалим его из списка
                self.clients.remove(client)

    def logMessage(self, message, client_address):
        # Записываем сообщение в лог с меткой времени
        try:
            with open("logs.txt", "a", encoding="utf-8") as log_file:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] {client_address} - {message.decode('utf-8')}\n")
        except Exception as e:
            print(f"Ошибка при записи в лог: {e}")

    def handle(self, client, client_address):
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.broadcastMessage(message, client_address)
                else:
                    break
            except:
                break

        self.clients.remove(client)
        client.close()

    def startLoop(self):
        while True:
            client, address = self.messagingServer.accept()
            self.clients.append(client)
            print(f"New connection from {address}")
            clientThread = threading.Thread(target=self.handle, args=(client, address))
            clientThread.start()
