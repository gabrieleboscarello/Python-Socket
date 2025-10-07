import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox

HOST = '127.0.0.1'
PORT = 9999

client_conn = None
server_socket = None
running = False

def start_server():
    global server_socket, client_conn, running
    running = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    text_log.insert(tk.END, f"Server in ascolto su {HOST}:{PORT}\n")

    def accept_connection():
        global client_conn
        client_conn, addr = server_socket.accept()
        text_log.insert(tk.END, f"Connessione stabilita con {addr}\n")
        receive_messages()

    threading.Thread(target=accept_connection, daemon=True).start()

def receive_messages():
    global client_conn, running
    def recv_loop():
        while running:
            try:
                data = client_conn.recv(1024).decode('utf-8')
                if not data:
                    break
                text_log.insert(tk.END, f" Client: {data}\n")
                text_log.see(tk.END)
            except:
                break
        text_log.insert(tk.END, "Connessione terminata.\n")

    threading.Thread(target=recv_loop, daemon=True).start()

def send_message():
    global client_conn
    msg = entry_message.get()
    if client_conn:
        client_conn.send(msg.encode('utf-8'))
        text_log.insert(tk.END, f"Tu: {msg}\n")
        entry_message.delete(0, tk.END)
        text_log.see(tk.END)
    else:
        messagebox.showwarning("Errore", "Nessun client connesso!")

def stop_server():
    global running, client_conn, server_socket
    running = False
    if client_conn:
        client_conn.close()
    if server_socket:
        server_socket.close()
    text_log.insert(tk.END, "Server chiuso.\n")

# --- GUI ---
root = tk.Tk()
root.title("ToodoMessage Server")
root.geometry("600x500")
root.configure(bg="#181818")

label_title = tk.Label(root, text="Server", font=("Helvetica", 18, "bold"), bg="#181818", fg="white")
label_title.pack(pady=10)

frame_buttons = tk.Frame(root, bg="#181818")
frame_buttons.pack(pady=5)

ttk.Button(frame_buttons, text="Avvia Server", command=start_server).grid(row=0, column=0, padx=5)
ttk.Button(frame_buttons, text="Chiudi Server", command=stop_server).grid(row=0, column=1, padx=5)

text_log = tk.Text(root, height=20, width=70, bg="#202020", fg="white", wrap="word")
text_log.pack(pady=10)

frame_send = tk.Frame(root, bg="#181818")
frame_send.pack(pady=5)

entry_message = ttk.Entry(frame_send, width=40)
entry_message.grid(row=0, column=0, padx=5)
ttk.Button(frame_send, text="Invia", command=send_message).grid(row=0, column=1, padx=5)

root.mainloop()
