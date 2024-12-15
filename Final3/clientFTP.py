import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def list_photos():
    photo_list = [f for f in os.listdir('.') if f.lower().endswith(('.jpg', '.jpeg'))]
    return photo_list

def send_photo():
    server_ip = entry_ip.get()
    server_port = int(entry_port.get())

    if not server_ip or not server_port:
        messagebox.showerror("Error", "Give valid IP address and Port.")
        return

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server_ip, server_port)
        client_socket.connect(server_address)
    except Exception as e:
        messagebox.showerror("Error", f"Cant connect to server: {e}")
        return

    if not photo_name:
        messagebox.showerror("Error", "Choose photo for send.")
        client_socket.close()
        return

    try:
        with open(photo_name, 'rb') as file:
            photo_data = file.read()

        client_socket.sendall(photo_data)
        messagebox.showinfo("Success", f"Photography '{photo_name}' successfully send to server.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{photo_name}' not found.")
    finally:
        client_socket.close()

def show_photos():
    photos = list_photos()
    if photos:
        photos_list.delete(0, tk.END)
        for p in photos:
            photos_list.insert(tk.END, p)
    else:
        messagebox.showinfo("Information", "Photos not found.")

def choose_photo():
    global photo_name
    photo_name = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg")])
    if photo_name:
        label_photo.config(text=f"Choosen photo: {os.path.basename(photo_name)}")
    else:
        label_photo.config(text="Photography not choosen.")

root = tk.Tk()
root.title("Photosender")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label_ip = tk.Label(frame_input, text="Servers IP address:")
label_ip.grid(row=0, column=0, padx=5)
entry_ip = tk.Entry(frame_input)
entry_ip.grid(row=0, column=1, padx=5)

label_port = tk.Label(frame_input, text="Servers Port:")
label_port.grid(row=1, column=0, padx=5)
entry_port = tk.Entry(frame_input)
entry_port.grid(row=1, column=1, padx=5)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

button_choose = tk.Button(frame_buttons, text="Choose photo", command=choose_photo)
button_choose.grid(row=0, column=0, padx=5)

button_send = tk.Button(frame_buttons, text="Send Photo", command=send_photo)
button_send.grid(row=0, column=1, padx=5)

label_photo = tk.Label(root, text="Photo not chosen.")
label_photo.pack(pady=10)

button_show = tk.Button(root, text="Show valid photos", command=show_photos)

button_show.pack(pady=10)

photos_list = tk.Listbox(root)

photos_list.pack(pady=10, fill=tk.BOTH, expand=True)

photo_name = ""

root.mainloop()
