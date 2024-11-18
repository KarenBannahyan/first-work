import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Функция для получения списка доступных фотографий в текущей директории
def list_photos():
    photo_list = [f for f in os.listdir('.') if f.lower().endswith(('.jpg', '.jpeg'))]
    return photo_list

# Функция для подключения и отправки фотографии
def send_photo():
    server_ip = entry_ip.get()
    server_port = int(entry_port.get())

    if not server_ip or not server_port:
        messagebox.showerror("Ошибка", "Пожалуйста, укажите правильный IP и порт.")
        return

    # Создаем сокет и подключаемся к серверу
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, server_port)
        client_socket.connect(server_address)
    except Exception as e:
        messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к серверу: {e}")
        return

    # Если выбрана фотография
    if not photo_name:
        messagebox.showerror("Ошибка", "Выберите фотографию для отправки.")
        client_socket.close()
        return

    try:
        with open(photo_name, 'rb') as file:
            photo_data = file.read()

        # Отправляем фотографию
        client_socket.sendall(photo_data)
        messagebox.showinfo("Успех", f"Фотография '{photo_name}' успешно отправлена на сервер.")
    except FileNotFoundError:
        messagebox.showerror("Ошибка", f"Файл '{photo_name}' не найден.")
    finally:
        client_socket.close()

# Функция для отображения доступных фотографий
def show_photos():
    photos = list_photos()
    if photos:
        photos_list.delete(0, tk.END)  # Очищаем список
        for p in photos:
            photos_list.insert(tk.END, p)
    else:
        messagebox.showinfo("Информация", "Фотографии не найдены.")

# Функция для выбора изображения через диалоговое окно
def choose_photo():
    global photo_name
    photo_name = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg")])
    if photo_name:
        label_photo.config(text=f"Выбрана фотография: {os.path.basename(photo_name)}")
    else:
        label_photo.config(text="Фотография не выбрана.")

# Инициализация окна
root = tk.Tk()
root.title("Фотоотправитель")

# Поля ввода для IP и порта
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_ip = tk.Label(frame_input, text="IP адрес сервера:")
label_ip.grid(row=0, column=0, padx=5)
entry_ip = tk.Entry(frame_input)
entry_ip.grid(row=0, column=1, padx=5)

label_port = tk.Label(frame_input, text="Порт сервера:")
label_port.grid(row=1, column=0, padx=5)
entry_port = tk.Entry(frame_input)
entry_port.grid(row=1, column=1, padx=5)

# Кнопки для выбора фото и отправки
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

button_choose = tk.Button(frame_buttons, text="Выбрать фотографию", command=choose_photo)
button_choose.grid(row=0, column=0, padx=5)

button_send = tk.Button(frame_buttons, text="Отправить фотографию", command=send_photo)
button_send.grid(row=0, column=1, padx=5)

# Метка для отображения выбранной фотографии
label_photo = tk.Label(root, text="Фотография не выбрана.")
label_photo.pack(pady=10)

# Кнопка для отображения списка доступных фотографий
button_show = tk.Button(root, text="Показать доступные фотографии", command=show_photos)
button_show.pack(pady=10)

# Список для отображения доступных фотографий
photos_list = tk.Listbox(root)
photos_list.pack(pady=10, fill=tk.BOTH, expand=True)

# Инициализация переменной для хранения имени выбранной фотографии
photo_name = ""

# Запуск основного цикла tkinter
root.mainloop()
