import socket
import os
import tkinter as tk
from tkinter import messagebox

def get_server_ip():
    return socket.gethostbyname(socket.gethostname())

def get_new_photo_filename():
    photo_dir = "received_photos"
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)

    existing_photos = [f for f in os.listdir(photo_dir) if f.lower().startswith("received_photo") and f.lower().endswith(".jpg")]
    new_photo_number = len(existing_photos) + 1
    return os.path.join(photo_dir, f"received_photo{new_photo_number}.jpg")

def start_server():
    port = int(entry_port.get())
    server_ip = get_server_ip()
    label_ip.config(text=f"IPv4 server address: {server_ip}")

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((server_ip, port))
        server_socket.listen(1)
        print("Server is on, waiting for connections...")
        listbox_log.insert(tk.END, "Server is on, waiting for connections...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Client is connected: {client_address}")
            listbox_log.insert(tk.END, f"Client connected: {client_address}")

            photo_data = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                photo_data += chunk

            photo_name = get_new_photo_filename()
            with open(photo_name, 'wb') as file:
                file.write(photo_data)

            print(f"Photography saved as {photo_name}")
            listbox_log.insert(tk.END, f"Photography saved as {photo_name}")
            client_socket.close()

    except Exception as e:
        listbox_log.insert(tk.END, f"Error: {str(e)}")
        messagebox.showerror("Error", f"Server error: {e}")

import threading
def start_server_thread():
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

root = tk.Tk()
root.title("Server for photos")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_port = tk.Label(frame_input, text="Enter port for server:")
label_port.grid(row=0, column=0, padx=5)
entry_port = tk.Entry(frame_input)
entry_port.grid(row=0, column=1, padx=5)

button_start = tk.Button(root, text="Run server", command=start_server_thread)
button_start.pack(pady=10)

label_ip = tk.Label(root, text="IPv4 servers address: Not found")
label_ip.pack(pady=10)

frame_log = tk.Frame(root)
frame_log.pack(pady=10)

listbox_log = tk.Listbox(frame_log, height=10, width=50)
listbox_log.pack(side=tk.LEFT, fill=tk.BOTH)
scrollbar_log = tk.Scrollbar(frame_log)
scrollbar_log.pack(side=tk.RIGHT, fill=tk.Y)

listbox_log.config(yscrollcommand=scrollbar_log.set)
scrollbar_log.config(command=listbox_log.yview)

root.mainloop()
