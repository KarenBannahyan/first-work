import socket
import os
import tkinter as tk
from tkinter import messagebox

# Функция для получения локального IP-адреса
def get_server_ip():
    return socket.gethostbyname(socket.gethostname())

# Функция для генерации уникального имени для сохраненной фотографии
def get_new_photo_filename():
    photo_dir = "received_photos"
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)

    existing_photos = [f for f in os.listdir(photo_dir) if f.lower().startswith("received_photo") and f.lower().endswith(".jpg")]
    new_photo_number = len(existing_photos) + 1
    return os.path.join(photo_dir, f"received_photo{new_photo_number}.jpg")

# Функция для старта сервера
def start_server():
    port = int(entry_port.get())
    server_ip = get_server_ip()
    label_ip.config(text=f"IPv4 адрес сервера: {server_ip}")

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, port))
        server_socket.listen(1)
        print("Сервер запущен, ожидание подключений...")
        listbox_log.insert(tk.END, "Сервер запущен, ожидание подключений...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключен клиент: {client_address}")
            listbox_log.insert(tk.END, f"Подключен клиент: {client_address}")

            photo_data = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                photo_data += chunk

            # Сохраняем фотографию с уникальным именем
            photo_name = get_new_photo_filename()
            with open(photo_name, 'wb') as file:
                file.write(photo_data)

            print(f"Фотография сохранена как {photo_name}")
            listbox_log.insert(tk.END, f"Фотография сохранена как {photo_name}")
            client_socket.close()

    except Exception as e:
        listbox_log.insert(tk.END, f"Ошибка: {str(e)}")
        messagebox.showerror("Ошибка", f"Ошибка запуска сервера: {e}")

# Функция для старта сервера в новом потоке
import threading
def start_server_thread():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

# Инициализация окна Tkinter
root = tk.Tk()
root.title("Сервер для получения фотографий")

# Поле ввода для порта сервера
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_port = tk.Label(frame_input, text="Введите порт для сервера:")
label_port.grid(row=0, column=0, padx=5)
entry_port = tk.Entry(frame_input)
entry_port.grid(row=0, column=1, padx=5)

# Кнопка для запуска сервера
button_start = tk.Button(root, text="Запустить сервер", command=start_server_thread)
button_start.pack(pady=10)

# Метка для отображения IP-адреса сервера
label_ip = tk.Label(root, text="IPv4 адрес сервера: Не определен")
label_ip.pack(pady=10)

# Список для отображения логов
frame_log = tk.Frame(root)
frame_log.pack(pady=10)

listbox_log = tk.Listbox(frame_log, height=10, width=50)
listbox_log.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar_log = tk.Scrollbar(frame_log)
scrollbar_log.pack(side=tk.RIGHT, fill=tk.Y)

listbox_log.config(yscrollcommand=scrollbar_log.set)
scrollbar_log.config(command=listbox_log.yview)

# Запуск главного цикла Tkinter
root.mainloop()
