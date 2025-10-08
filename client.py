#Librerie
import socket                       
import threading                   
import tkinter as tk
from tkinter import ttk, messagebox

# Indirizzo e porta del server 
HOST = '127.0.0.1'  # localhost (stesso computer)
PORT = 9999

# Variabili globali per il socket e lo stato della connessione
client_socket = None
connected = False

def connect_to_server():
    global client_socket, connected # specifico che voglio lavorare con variabili globali
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # crea il socket TCP (Ipv4, TCP)
        client_socket.connect((HOST, PORT))  # tenta la connessione al server
        connected = True
        text_log.insert(tk.END, f" Connesso al server {HOST}:{PORT}\n")  # piccolo messaggio che indica all'utente l'indirizzo e la porta del server
        # avvio un thread in background per ricevere messaggi e contemporaneamente mostra l'interfaccia fluida
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        # se la connessione fallisce mostro un messaggio d'errore
        messagebox.showerror("Errore", f"Impossibile connettersi: {e}")

def receive_messages():
    """Ho creato un loop che rimane sempre in ascolto dei messaggi inviati dal server.
        Appena L'utente Server chiude la connessione il ciclo si interrompe.
       """
    global client_socket, connected
    while connected:
        try:
            # ricevo fino ad un massimo di 1024 byte e traduci i bytes in stringa UTF-8
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                # se recv() è vuoto vuol dire che il server a chiuso connessione 
                break
            # mostra il messaggio ricevuto 
            text_log.insert(tk.END, f"Server: {data}\n")
            text_log.see(tk.END)  # scorri in basso per mostrare l'ultimo messaggio
        except:
            # se c'è un errore esco dal loop subito
            break
    text_log.insert(tk.END, "Connessione chiusa da parte del server.\n")

def send_message():
    global client_socket, connected
    msg = entry_message.get()  # prendo il messaggio che viene scritto dall'utente
    if connected:
        client_socket.send(msg.encode('utf-8'))  # invio il messaggio codificato
        text_log.insert(tk.END, f" Tu: {msg}\n")  # mostro quello che ho inviato
        entry_message.delete(0, tk.END)  # pulisco la casella di testo eliminando il contenuto
        text_log.see(tk.END)
    else:
        messagebox.showwarning("Attenzione", "Non sei connesso al server!")

def disconnect():
    global client_socket, connected
    connected = False               # segnalo al thread di fermarsi
    if client_socket:
        client_socket.close()       # chiudo il socket
    text_log.insert(tk.END, " Disconnesso.\n")

# ================= PARTE GRAFICA =================
root = tk.Tk()
root.title("ToodoMessage Client")
root.geometry("600x500")
root.configure(bg="#181818")  # colore di sfondo della finestra

# titolo in alto
label_title = tk.Label(root, text="Client", font=("Helvetica", 18, "bold"), bg="#181818", fg="white")
label_title.pack(pady=10)

# frame che contiene i pulsanti Connetti / Disconnetti
frame_buttons = tk.Frame(root, bg="#181818")
frame_buttons.pack(pady=5)

ttk.Button(frame_buttons, text="Connetti", command=connect_to_server).grid(row=0, column=0, padx=5)
ttk.Button(frame_buttons, text="Disconnetti", command=disconnect).grid(row=0, column=1, padx=5)

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
