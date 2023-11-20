import socket
import threading
import tkinter as tk

HOST = '127.0.0.1'
PORT = 5555
LISTENER_LIMIT = 5
active_clients = []  

DARK_GREY = '#18191a'
WHITE = "white"
FONT = ("Helvetica", 12)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

root = tk.Tk()
root.title("Server")
root.geometry("300x200")
root.configure(bg=DARK_GREY)

status_label = tk.Label(root, text="Server Status", font=FONT, fg=WHITE, bg=DARK_GREY)
status_label.pack(pady=10)

info_text = tk.Text(root, height=8, width=30, font=FONT, fg=WHITE, bg=DARK_GREY)
info_text.pack(pady=10)
info_text.config(state=tk.DISABLED)

def update_info(message):
    info_text.config(state=tk.NORMAL)
    info_text.insert(tk.END, message + '\n')
    info_text.config(state=tk.DISABLED)

def listen_for_messages(client, username):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print(f"The message sent from client {username} is empty")

def send_message_to_client(client, message):
    client.sendall(message.encode())


def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

def client_handler(client):
    while True:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} joined the convo"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username,)).start()

def main():
    server.listen(LISTENER_LIMIT)
    update_info(f"Running the server on {HOST} {PORT}")

    while True:
        client, address = server.accept()
        update_info(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client,)).start()

if __name__ == '__main__':
    threading.Thread(target=main).start()
    root.mainloop()
