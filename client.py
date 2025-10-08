import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox

HOST = '127.0.0.1'
PORT = 9999

client_socket = None
connected = False

def connect_to_server():
    global client_socket, connected
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        connected = True
        text_log.insert(tk.END, f" Connesso al server {HOST}:{PORT}\n")
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile connettersi: {e}")

def receive_messages():
    global client_socket, connected
    while connected:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            text_log.insert(tk.END, f"Server: {data}\n")
            text_log.see(tk.END)
        except:
            break
    text_log.insert(tk.END, "Connessione chiusa da parte del server.\n")

def send_message():
    global client_socket, connected
    msg = entry_message.get()
    if connected:
        client_socket.send(msg.encode('utf-8'))
        text_log.insert(tk.END, f" Tu: {msg}\n")
        entry_message.delete(0, tk.END)
        text_log.see(tk.END)
    else:
        messagebox.showwarning("Attenzione", "Non sei connesso al server!")

def disconnect():
    global client_socket, connected
    connected = False
    if client_socket:
        client_socket.close()
    text_log.insert(tk.END, " Disconnesso.\n")

#PARTE GRAFICA
root = tk.Tk()
root.title("ToodoMessage Client")
root.geometry("600x500")
root.configure(bg="#181818")

label_title = tk.Label(root, text="Client", font=("Helvetica", 18, "bold"), bg="#181818", fg="white")
label_title.pack(pady=10)

frame_buttons = tk.Frame(root, bg="#181818")
frame_buttons.pack(pady=5)

ttk.Button(frame_buttons, text="Connetti", command=connect_to_server).grid(row=0, column=0, padx=5)
ttk.Button(frame_buttons, text="Disconnetti", command=disconnect).grid(row=0, column=1, padx=5)

text_log = tk.Text(root, height=20, width=70, bg="#202020", fg="white", wrap="word")
text_log.pack(pady=10)

frame_send = tk.Frame(root, bg="#181818")
frame_send.pack(pady=5)

entry_message = ttk.Entry(frame_send, width=40)
entry_message.grid(row=0, column=0, padx=5)
ttk.Button(frame_send, text="Invia", command=send_message).grid(row=0, column=1, padx=5)

root.mainloop()

