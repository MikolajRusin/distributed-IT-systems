import socket
import threading
from argparse import ArgumentParser
from dataclasses import dataclass, field

@dataclass
class ChatClient:
    server_ip: str
    server_port: int
    buffer_size: int = 1024

    def __post_init__(self):
        self.__actions = {
            '+':self.register,
            '-': self.unregister,
            '?': self.show_username,
            '!': self.send_message
        }
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.execute_action('+')
        threading.Thread(target=self.listen, daemon=True).start()

        while True:
            print('Choose action')
            print('- -> Unregister')
            print('? -> Show Username')
            print('! -> Send Message')

            choice = input('Your Choice: ')
            self.execute_action(choice)
            
    def listen(self):
        while True:
            data, _ = self.sock.recvfrom(self.buffer_size)
            print(f'\nReceived from Server: {data.decode()}')

    def register(self):
        self.username = input('Provide Your Username: ')
        register_message = f'+ | {self.username} |'
        self.sock.sendto(register_message.encode(), (self.server_ip, self.server_port))
    
    def unregister(self):
        unregister_message = f'- | {self.username} |'
        self.sock.sendto(unregister_message.encode(), (self.server_ip, self.server_port))

    def show_username(self):
        user_filter = input('Provide username to show ')
        show_user_message = f'? | {user_filter} |'
        self.sock.sendto(show_user_message.encode(), (self.server_ip, self.server_port))

    def send_message(self):
        receiver = input('Receiver: ')
        message = input('Message: ')
        data_to_send = f'! | {receiver} | {self.username} | {message} |'
        self.sock.sendto(data_to_send.encode(), (self.server_ip, self.server_port))

    def execute_action(self, key):
        action = self.__actions[key]
        action()

if __name__ == '__main__':
    args_parser = ArgumentParser()
    args_parser.add_argument('--server_ip', type=str, help='IP')
    args_parser.add_argument('--server_port', type=int, help='Port')
    args = args_parser.parse_args()

    client = ChatClient(server_ip=args.server_ip, server_port=args.server_port)
    client.start()
