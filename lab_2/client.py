import Pyro5
from Pyro5.api import Proxy, expose
from dataclasses import dataclass, field
import threading

@expose
@dataclass
class ClientRemote:
    registered: bool = field(default=False, init=False)

    def successful_registration(self, status: bool):
        if not status:
            print(f'{status}: Nickname already exist. Please provide another nickname')
        else:
            print(f'{status}: Nickname has been registered')
            
        self.registered = status
    
    def successful_unregistration(self, status: bool):
        print(f'{status}: User has been unregistered')
        self.registered = False

    def show_clients(self, clients: list):
        print(clients)

    def receive_message(self, sender, receiver, message):
        print(f'\n\nSender: {sender}\nReceiver: {receiver}\nMessage: {message}')

@dataclass
class Client:

    def __post_init__(self):
        self.server_proxy = Pyro5.api.Proxy('PYRONAME:mini_chat')

        self.daemon = Pyro5.api.Daemon()
        self.client_remote = ClientRemote()
        self.client_uri = self.daemon.register(self.client_remote)
        threading.Thread(target=self.daemon.requestLoop, daemon=True).start()

        self.__actions = {
            '+': self.register,
            '-': self.unregister,
            '?': self.show_username,
            '!': self.send_message
        }

    def start(self):
        while True:
            while not self.client_remote.registered:
                self.execute_action('+')

            print('Choose action')
            print('- -> Unregister')
            print('? -> Show Username')
            print('! -> Send Message')

            choice = input('Your choice: ')
            self.execute_action(choice)
                
    def execute_action(self, key):
        action = self.__actions[key]
        action()

    def register(self):
        self.client_name = input('Provide nickname: ').strip()
        self.server_proxy.client_register(self.client_name, str(self.client_uri))

    def unregister(self):
        self.server_proxy.client_unregister(self.client_name)

    def show_username(self):
        nickname_filter = input('Enter a nickname to display users with that nickname or a similar one: ').strip()
        self.server_proxy.filter_clients(self.client_name, nickname_filter)

    def send_message(self):
        receiver = input('Receiver: ')
        message = input('Message: ')
        self.server_proxy.send_message(self.client_name, receiver, message)

def main():
    client = Client()
    client.start()

if __name__ == '__main__':
    main()