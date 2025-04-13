import socket
from datetime import datetime
from dataclasses import dataclass, field
from argparse import ArgumentParser

@dataclass
class ChatServer:
    ip: str
    port: int
    clients: dict = field(default_factory=dict)
    buffer_size: int = 1024

    def __post_init__(self):
        self.__actions = {
            '+': self.client_register,
            '-': self.client_unregister,
            '?': self.show_clients,
            '!': self.send_message
        }

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))

    def start(self):
        while True:
            received_data, addr = self.sock.recvfrom(self.buffer_size)
            data = received_data.decode().split('|')
            print(data)
            action = data[0].replace(' ', '')
            self.execute_action(action, data, addr)

    def client_register(self, data: list, addr):
        client_username = data[1].replace(' ', '')
        self.clients[client_username] = addr

        message = '|'.join(data) + ' OK |'
        self.server_resend_message(message, addr)

    def client_unregister(self, data, addr):
        client_username = data[1].replace(' ', '')
        self.clients.pop(client_username)

        message = '|'.join(data) + ' OK |'
        self.server_resend_message(message, addr)

    def show_clients(self, data, addr):
        filter_username = data[1].replace(' ', '')
        if data[1] == '':
            clients_list = list(self.clients.keys())
        else:
            clients_list = [user.replace(' ', '') for user in self.clients.keys() if filter_username in user]

        message = '|'.join(data) + ' ' + ' '.join(clients_list) + ' | ' + 'OK |'
        self.server_resend_message(message, addr)

    def send_message(self, data, addr):
        receiver = data[1].replace(' ', '')
        sender = data[2].replace(' ', '')
        message_from_sender = data[3]

        receiver_message = f'User: {sender}\nMessage: {message_from_sender}'
        sender_message = f'| {receiver} | {sender} | OK |'
        self.sock.sendto(receiver_message.encode(), self.clients[receiver])
        self.server_resend_message(sender_message, addr)

    def server_resend_message(self, message: list, addr):
        self.sock.sendto(message.encode(), addr)

    def execute_action(self, key, data, addr):
        action = self.__actions[key]
        action(data, addr)

if __name__ == '__main__': 
    args_parser = ArgumentParser()
    args_parser.add_argument('--ip', type=str, help='IP')
    args_parser.add_argument('--port', type=int, help='Port')
    args = args_parser.parse_args()

    server = ChatServer(ip=args.ip, port=args.port)
    server.start()

