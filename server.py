import socket
import threading
import tkinter as tk

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []

DARK_GREY = '#18191a'
MEDIUM_GREY = '#242526'
OCEAN_BLUE = '#3a3b3c'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.root = tk.Tk()

        self.root.title("Chat Server")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=4)
        self.root.grid_rowconfigure(2, weight=1)

        self.top_frame = tk.Frame(self.root, width=400, height=50, bg=DARK_GREY)
        self.top_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.middle_frame = tk.Frame(self.root, width=400, height=200, bg=MEDIUM_GREY)
        self.middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.bottom_frame = tk.Frame(self.root, width=400, height=50, bg=DARK_GREY)
        self.bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

        self.start_server_button = tk.Button(self.bottom_frame, text="Start Server", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=self.start_server)
        self.start_server_button.pack(pady=10)

        self.message_box = tk.Text(self.middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=40, height=10)
        self.message_box.config(state=tk.DISABLED)
        self.message_box.pack(side=tk.TOP)

        self.server_running = False

    def add_message(self, message):
        self.message_box.config(state=tk.NORMAL)
        self.message_box.insert(tk.END, message + '\n')
        self.message_box.config(state=tk.DISABLED)

    def start_server(self):
        self.server.bind((HOST, PORT))
        self.add_message(f"Running the server on {HOST} {PORT}")
        self.server.listen(LISTENER_LIMIT)
        self.add_message("Server is now listening for connections...")
        self.server_running = True
        threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):
        while self.server_running:
            try:
                client, address = self.server.accept()
                self.add_message(f"Successfully connected to client {address[0]} {address[1]}")
                threading.Thread(target=self.client_handler, args=(client,)).start()
            except Exception as e:
                print(f"Error accepting connections: {str(e)}")

    def client_handler(self, client):
        while self.server_running:
            try:
                username = client.recv(2048).decode('utf-8')
                if username != '':
                    active_clients.append((username, client))
                    prompt_message = f"[SERVER] {username} joined the chat"
                    self.send_messages_to_all(prompt_message)
                    break
                else:
                    print("Client username is empty")
            except Exception as e:
                print(f"Error receiving username: {str(e)}")

        self.listen_for_messages(client, username)

    def listen_for_messages(self, client, username):
        while self.server_running:
            try:
                message = client.recv(2048).decode('utf-8')
                if message != '':
                    final_msg = username + '~' + message
                    self.send_messages_to_all(final_msg)
                else:
                    print(f"The message send from client {username} is empty")
            except Exception as e:
                print(f"Error receiving message from {username}: {str(e)}")
                break

    def send_messages_to_all(self, message):
        for user in active_clients:
            self.send_message_to_client(user[1], message)

    def send_message_to_client(self, client, message):
        try:
            client.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to client: {str(e)}")

    def main(self):
        self.root.mainloop()

if __name__ == '__main__':
    chat_server = ChatServer()
    chat_server.main()
