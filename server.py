# Librerie
import socket                       
import threading                   
import tkinter as tk
from tkinter import ttk, messagebox

HOST = '127.0.0.1'  # localhost (stesso computer)
PORT = 9999

# Variabili globali per il socket, la connessione e lo stato del server
client_conn = None
server_socket = None
running = False

def start_server():
    global server_socket, client_conn, running  # specifico che voglio lavorare con variabili globali
    running = True
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # crea socket TCP (IPv4, TCP)
        server_socket.bind((HOST, PORT))  # collega il socket all’indirizzo e alla porta
        server_socket.listen(1)  # il server accetta una connessione alla volta (Valore Modificabile in base a quante connessioni vogliamo, grazie alla libreria threading)
        text_log.insert(tk.END, f" Server in ascolto su {HOST}:{PORT}\n")

       
        def accept_connection():
            global client_conn
            client_conn, addr = server_socket.accept()  # accetta la connessione del client
            text_log.insert(tk.END, f" Connessione stabilita con {addr}\n")
            receive_messages()
            
     # Thread che accetta le connessioni senza bloccare la GUI
        threading.Thread(target=accept_connection, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile avviare il server: {e}")

def receive_messages():
    """Loop che rimane sempre in ascolto dei messaggi ricevuti dal client.
       Quando il client chiude la connessione, il ciclo termina automaticamente."""
    global client_conn, running

    def recv_loop():
        while running:
            try:
                # ricevo fino a 1024 byte e li decodifico da bytes a stringa UTF-8
                data = client_conn.recv(1024).decode('utf-8')
                if not data:
                    break
                # mostra il messaggio ricevuto dal client
                text_log.insert(tk.END, f" Client: {data}\n")
                text_log.see(tk.END)  
            except:
                # se c’è un errore esco subito dal loop
                break
        text_log.insert(tk.END, " Connessione terminata.\n")

    # avvio il thread che gestisce la ricezione per non bloccare l’interfaccia
    threading.Thread(target=recv_loop, daemon=True).start()

def send_message():
    """Prende il messaggio scritto dal server e lo invia al client (se connesso)."""
    global client_conn
    msg = entry_message.get()  # prendo il messaggio scritto dall'utente (server)
    if client_conn:
        client_conn.send(msg.encode('utf-8'))  # invio il messaggio codificato in UTF-8
        text_log.insert(tk.END, f" Tu: {msg}\n")  # mostro ciò che ho inviato
        entry_message.delete(0, tk.END)  # pulisco la casella di testo
        text_log.see(tk.END)
    else:
        messagebox.showwarning("Errore", "Nessun client connesso!")

def stop_server():
    """Chiude la connessione e ferma il server in modo sicuro."""
    global running, client_conn, server_socket
    running = False               # ferma il loop di ricezione
    if client_conn:
        client_conn.close()       # chiudo la connessione
    if server_socket:
        server_socket.close()     # chiudo il socket
    text_log.insert(tk.END, " Server chiuso.\n")

# ================= PARTE GRAFICA =================
root = tk.Tk()
root.title("ToodoMessage Server")
root.geometry("600x500")
root.configure(bg="#181818")  # colore di sfondo della finestra

# titolo in alto
label_title = tk.Label(root, text="Server", font=("Helvetica", 18, "bold"), bg="#181818", fg="white")
label_title.pack(pady=10)

# frame che contiene i pulsanti Avvia / Chiudi Server
frame_buttons = tk.Frame(root, bg="#181818")
frame_buttons.pack(pady=5)

ttk.Button(frame_buttons, text="Avvia Server", command=start_server).grid(row=0, column=0, padx=5)
ttk.Button(frame_buttons, text="Chiudi Server", command=stop_server).grid(row=0, column=1, padx=5)

# area testuale che funge da log delle comunicazioni
text_log = tk.Text(root, height=20, width=70, bg="#202020", fg="white", wrap="word")
text_log.pack(pady=10)

# frame per inviare messaggi: entry + bottone Invia
frame_send = tk.Frame(root, bg="#181818")
frame_send.pack(pady=5)

entry_message = ttk.Entry(frame_send, width=40)
entry_message.grid(row=0, column=0, padx=5)
ttk.Button(frame_send, text="Invia", command=send_message).grid(row=0, column=1, padx=5)

# avvia la GUI
root.mainloop()

