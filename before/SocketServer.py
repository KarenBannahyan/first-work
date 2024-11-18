import threading
from socket import socket, AF_INET, SOCK_STREAM

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

    def broadcastMessage(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            message = client.recv(1024)
            self.broadcastMessage(message)

    def startLoop(self):
        while True:
            client, address = self.messagingServer.accept()
            self.clients.append(client)
            clientThread = threading.Thread(target=self.handle, args=(client,))
            clientThread.start()
