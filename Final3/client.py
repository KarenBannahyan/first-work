import mysql.connector
import logging
import socket
import threading as thread
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess  # for clientftp.py
from vidstream import ScreenShareClient
from ClientSocket import ClientSocket

ipAddressEditText = None
portEditText = None
startListeningButton = None
stopListeningButton = None
connectionStatusText = None
window = None
login_window = None
password_entry = None

def get_passwords_from_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Karen1234",
            database="users"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM passwords")
        passwords = cursor.fetchall()

        password_list = [pwd[0] for pwd in passwords]

        cursor.close()
        connection.close()

        return password_list

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []


def check_password():
    password = password_entry.get()
    passwords = get_passwords_from_db()

    if password in passwords:
        login_window.destroy()
        startWindow()
    else:
        messagebox.showerror("Incorrect Password", "The password you entered is incorrect.")

def open_password_window():
    global login_window, password_entry

    login_window = tk.Tk()
    login_window.title("Enter Password")
    login_window.geometry("300x150")

    password_label = tk.Label(login_window, text="Enter password:")
    password_label.pack(pady=10)

    password_entry = tk.Entry(login_window, show="*", width=20)
    password_entry.pack(pady=10)

    login_button = tk.Button(login_window, text="Login", command=check_password)
    login_button.pack(pady=10)

    login_window.mainloop()

def startServer():
    global ipAddress, port
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
                                 "We were unable to start streaming to provided IP address, check whether client is "
                                 "listening to this IP address and if IP address is correct")
        except ValueError:
            messagebox.showerror("Incorrect port number",
                                 "Port number can only be numbers")
        except Exception:
            logging.exception("An exception was thrown!")

def startWindow():
    global window, ipAddressEditText, portEditText, startListeningButton, stopListeningButton, connectionStatusText

    window = tk.Tk()
    window.title = "Screen Share"
    window.geometry("500x500")

    ipAddressLabel = tk.Label(window, text="Enter IP Address to start screen sharing (Same IP as server's) : ")
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

    sendPhotoButton = tk.Button(window, text="Send photo", width=50, command=sendPhoto)
    sendPhotoButton.pack(anchor=tk.CENTER, pady=10)

    connectionStatusText = tk.Label(window, text="No Active Connections...")
    connectionStatusText.pack(pady=20)

    sep = ttk.Separator(window, orient='horizontal')
    sep.pack(fill='x')

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

def sendPhoto():
    try:
        subprocess.run(['python', 'clientftp.py'], check=True)
        messagebox.showinfo("Success", "Photo successfully sent.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unknown error: {e}")


open_password_window()
