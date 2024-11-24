import threading
from socket import socket, AF_INET, SOCK_STREAM
import mysql.connector
from datetime import datetime
from ClientSocket import ClientSocket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

class SocketServer:

    def __init__(self, host, port):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Karen1234',
            'database': 'users',
        }
        self.db_connection = mysql.connector.connect(**self.db_config)
        self.cursor = self.db_connection.cursor()
        self.ipAddress = host
        self.messagingServer = socket(AF_INET, SOCK_STREAM)
        self.messagingServer.bind((host, port))
        self.messagingServer.listen()

        self.clients = []
        self.clientSocket = ClientSocket(host, port, True)
        self.startLoop()

    def broadcastMessage(self, message, client_address):
        self.logMessage(message, client_address)

        for client in self.clients:
            try:
                client.send(message)
            except:
                self.clients.remove(client)

    def logMessage(self, message, client_address):
        encrypted_message, key, iv = self.hash_text(message.decode('utf-8'))

        self.save_key_iv_to_file(client_address, key, iv, encrypted_message)

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            query = "INSERT INTO logs (timestamp, client_address, message) VALUES (%s, %s, %s)"
            values = (timestamp, str(client_address), encrypted_message)

            self.cursor.execute(query, values)
            self.db_connection.commit()
        except mysql.connector.Error as e:
            print(f"Ошибка при записи в базу данных: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

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

    def hash_text(self, plain_text):

        key = os.urandom(32)
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padding_length = 16 - len(plain_text) % 16
        padded_text = plain_text + chr(padding_length) * padding_length

        encrypted_text = encryptor.update(padded_text.encode()) + encryptor.finalize()

        return base64.b64encode(encrypted_text).decode('utf-8'), base64.b64encode(key).decode(
            'utf-8'), base64.b64encode(iv).decode('utf-8')

    def unhash_text(self, encrypted_text_b64, key_b64, iv_b64):
        try:
            encrypted_text = base64.b64decode(encrypted_text_b64)
            key = base64.b64decode(key_b64)
            iv = base64.b64decode(iv_b64)

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()

            padding_length = decrypted_text[-1]
            decrypted_text = decrypted_text[:-padding_length].decode('utf-8')

            return decrypted_text

        except Exception as e:
            return f"Ошибка: {str(e)}"

    def save_key_iv_to_file(self, client_address, key, iv, encrypted_message):
        try:
            with open("logs.txt", "a") as f:
                f.write(f"Client IP: {client_address}\n")
                f.write(f"Key: {key}\n")
                f.write(f"IV: {iv}\n")
                f.write(f"Encrypted Message: {encrypted_message}\n\n")
        except Exception as e:
            print(f"Ошибка при сохранении ключа и IV в файл: {e}")

    def read_key_iv_from_file(self):
        try:
            with open("logs.txt", "r") as f:
                lines = f.readlines()
                if len(lines) >= 4:
                    ip = lines[-4].strip().split(": ")[1]
                    key = lines[-3].strip().split(": ")[1]
                    iv = lines[-2].strip().split(": ")[1]
                    return ip, key, iv
                else:
                    print("Ошибка: Недостаточно данных в файле logs.txt.")
                    return None, None, None
        except Exception as e:
            print(f"Ошибка при чтении ключа и IV из файла: {e}")
            return None, None, None

    def close(self):
        self.cursor.close()
        self.db_connection.close()
