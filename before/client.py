
# This is a sample Python script.
import logging
import socket
import threading as thread
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from vidstream import ScreenShareClient

from ClientSocket import ClientSocket


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
            server = ScreenShareClient(ipAddress, int(port))
            runner = thread.Thread(target=server.start_stream())
            runner.start()
            setConnectionStatus(f"Started screen streaming to {ipAddress} with port: {port}")
            switchButtOnStates(True)
            ClientSocket(ipAddress, 9090, False)
        except socket.gaierror:
            messagebox.showerror("IP address Not resolved",
                                 "Unable to resolve IP address, check if IP address is correct and it is accessible")
        except ConnectionRefusedError:
            messagebox.showerror("Unable to start streaming",
                                 "We were unable to start streaming to provided IP address,check whether client is "
                                 "listening to this IP address and if IP address is correct")
        except ValueError:
            messagebox.showerror("Incorrect port number",
                                 "Port number can only be numbers")
        except Exception:
            logging.exception("An exception was thrown!")


def startWindow():
    window.mainloop()


def stopServer():
    stopper = thread.Thread(target=server.stop_stream())
    stopper.start()
    exit()
    setConnectionStatus(f"Stopped screen streaming to {ipAddress}")
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


window = tk.Tk()
window.title = "Screen Share"
window.geometry("500x500")

ipAddressLabel = tk.Label(window,
                          text="Enter IP Address to start screen sharing (Same IP as server's) : ")
ipAddressLabel.pack()
ipAddressEditText = tk.Entry(window, width=window.winfo_screenwidth())
ipAddressEditText.pack(padx=20, pady=10)

portLabel = tk.Label(window, text="Enter Port number (Same port number as the server's): ")
portLabel.pack()

portEditText = tk.Entry(window, width=window.winfo_screenwidth())
portEditText.pack(padx=20, pady=10)

startListeningButton = tk.Button(window, text="Start Screen Sharing", width=50, command=startServer)
startListeningButton.pack(anchor=tk.CENTER, pady=10)

stopListeningButton = tk.Button(window, text="Stop Screen Sharing", width=50, command=stopServer)
stopListeningButton.pack(anchor=tk.CENTER)
stopListeningButton["state"] = "disabled"

connectionStatusText = tk.Label(window, text="No Active Connections...")
connectionStatusText.pack(pady=20)

sep = ttk.Separator(window, orient='horizontal')
sep.pack(fill='x')

global ipAddress
global server
global port

startWindow()
