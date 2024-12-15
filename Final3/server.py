
import logging
import socket
import threading as thread
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess

from vidstream import StreamingServer
from SocketServer import SocketServer

def startServer():
    global ipAddress
    global port
    ipAddress = ipAddressEditText.get()
    port = portEditText.get()
    if ipAddress == "":
        messagebox.showerror("IP Address is empty", "Ip Address cannot be empty, please insert valid ip address")
    else:
        global server
        try:
            server = StreamingServer(ipAddress, int(port))
            runner = thread.Thread(target=server.start_server)  # Исправлено
            runner.start()
            setConnectionStatus(f"Listening to {ipAddress} with port: {port}")
            switchButtOnStates(True)

            # Запуск SocketServer в отдельном потоке
            socket_server_thread = thread.Thread(target=SocketServer, args=(ipAddress, 9090))
            socket_server_thread.start()

        except socket.gaierror:
            messagebox.showerror("IP address Not resolved",
                                 "Unable to resolve IP address, check if IP address is correct and it is accessible")
        except ValueError:
            messagebox.showerror("Incorrect port number",
                                 "Port number can only be numbers")
        except Exception:
            logging.exception("An exception was thrown!")

def startWindow():
    window.mainloop()

def stopServer():
    server.stop_server()
    setConnectionStatus(f"Stopped listening to {ipAddress}")
    switchButtOnStates(False)

def switchButtOnStates(listening):
    if listening:
        startListeningButton["state"] = "disabled"
        stopListeningButton["state"] = "normal"
    else:
        startListeningButton["state"] = "normal"
        stopListeningButton["state"] = "disabled"

def setConnectionStatus(status):
    connectionStatusText["text"] = status

def receivePhoto():
    try:
        subprocess.run(['python', 'serverftp.py'], check=True)
        messagebox.showinfo("Success", "Photo successfully send.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unknown error: {e}")

window = tk.Tk()
window.title = "Screen Share"
window.geometry("450x450")

ipAddressLabel = tk.Label(window, text="Enter IP Address to listen for incoming connections : ")
ipAddressLabel.pack()

ipAddressEditText = tk.Entry(window, width=window.winfo_screenwidth())
ipAddressEditText.pack(padx=20, pady=10)

portLabel = tk.Label(window, text="Enter port number (Do not use 9090 as it is going to be reserved): ")
portLabel.pack()

portEditText = tk.Entry(window, width=window.winfo_screenwidth())
portEditText.pack(padx=20, pady=10)

startListeningButton = tk.Button(window, text="Start listening", width=50, command=startServer)
startListeningButton.pack(anchor=tk.CENTER, pady=10)

stopListeningButton = tk.Button(window, text="Stop listening", width=50, command=stopServer)
stopListeningButton.pack(anchor=tk.CENTER)
stopListeningButton["state"] = "disabled"

receivePhotoButton = tk.Button(window, text="Get photo", width=50, command=receivePhoto)
receivePhotoButton.pack(anchor=tk.CENTER, pady=10)

connectionStatusText = tk.Label(window, text="No Active Connections...")
connectionStatusText.pack(pady=20)

sep = ttk.Separator(window, orient='horizontal')
sep.pack(fill='x')

global ipAddress
global server
global messagingServer
global port
global messagingBroadcaster

startWindow()
