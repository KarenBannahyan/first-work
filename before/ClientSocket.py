import socket
import threading
import tkinter as tk
import tkinter.scrolledtext


class ClientSocket:

    def __init__(self, host, port, isServer):
        self.isServer = isServer
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        message = tk.Tk()
        message.withdraw()

        self.isRunning = True
        self.guiDone = False

        guiThread = threading.Thread(target=self.guiLoop)
        receiveThread = threading.Thread(target=self.receive)

        guiThread.start()
        receiveThread.start()

    def guiLoop(self):
        self.win = tk.Tk()
        self.win.config(bg="lightgray")

        self.chatLabel = tk.Label(self.win, text="Chat", bg="lightgray")
        self.chatLabel.pack(padx=20, pady=5)

        self.textArea = tkinter.scrolledtext.ScrolledText(self.win)
        self.textArea.pack(padx=20, pady=5)
        self.textArea.config(state="disabled")

        if self.isServer:
            self.input = tk.Text(self.win, height=3)
            self.input.pack(padx=20, pady=5)
            self.sendButton = tk.Button(self.win, text="Send", command=self.write)
            self.sendButton.pack(padx=20, pady=5)

        self.guiDone = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def stop(self):
        self.isRunning = False
        self.win.destroy()
        self.client.close()
        exit(0)

    def write(self):
        message = f"{self.input.get('1.0', 'end')}"
        self.client.send(message.encode("utf-8"))
        self.input.delete("1.0", "end")

    def receive(self):
        while self.isRunning:
            message = self.client.recv(1024)
            if self.guiDone:
                if self.isServer:
                    self.textArea.config(state="normal")
                    self.textArea.insert("end", "Message to all clients: " + message.decode("utf-8"))
                    self.textArea.yview("end")
                    self.textArea.config(state="disabled")
                else:
                    self.textArea.config(state="normal")
                    self.textArea.insert("end", "Server: " + message.decode("utf-8"))
                    self.textArea.yview("end")
                    self.textArea.config(state="disabled")

    def addMessage(self, message):
        self.textArea.config(state="normal")
        self.textArea.insert("end", "Message to all clients: " + message.decode("utf-8"))
        self.textArea.yview("end")
        self.textArea.config(state="disabled")
