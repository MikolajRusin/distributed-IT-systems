import Pyro5
from Pyro5.api import expose
from dataclasses import dataclass, field

@dataclass
class Server:
    clients: dict = field(default_factory=dict)

    def __post_init__(self):
        # Create Pyro Daemon
        daemon = Pyro5.api.Daemon()
        ns = Pyro5.api.locate_ns()                  # Find the name server
        server_remote = RemoteObjects(self)
        uri = daemon.register(server_remote)        # Register the server objects as a Pyro objects
        ns.register('mini_chat', uri)               # Register the object with a name in the name server

        # Start Pyro server
        print('Server URI:', uri)
        daemon.requestLoop()

    def client_register(self, name: str, uri: str):
        client_proxy = Pyro5.api.Proxy(uri)
        if name not in list(self.clients.keys()):    
            self.clients[name] = uri
            client_proxy.successful_registration(True)
        else:
            client_proxy.successful_registration(False)

    def client_unregister(self, name: str):
        client_uri = self.clients[name]
        client_proxy = Pyro5.api.Proxy(client_uri)
        self.clients.pop(name)
        client_proxy.successful_unregistration(True)

    def filter_clients(self, name: str, nickname_filter: str):
        client_uri = self.clients[name]
        client_proxy = Pyro5.api.Proxy(client_uri)
        filtered_nicknames = [client for client in self.clients if nickname_filter in client] if nickname_filter else list(self.clients)
        client_proxy.show_clients(filtered_nicknames)

    def send_message(self, sender: str, receiver: str, message: str):
        receiver_uri = self.clients[receiver]
        receiver_proxy = Pyro5.api.Proxy(receiver_uri)
        receiver_proxy.receive_message(sender, receiver, message)

@expose
@dataclass
class RemoteObjects:
    server: Server
    
    def client_register(self, name: str, uri: str):
        self.server.client_register(name, uri)

    def client_unregister(self, name: str):
        self.server.client_unregister(name)
    
    def filter_clients(self, name: str, nickname_filter: str):
        self.server.filter_clients(name, nickname_filter)

    def send_message(self, sender: str, receiver: str, message: str):
        self.server.send_message(sender, receiver, message)

def main():
    server = Server()
    server.start_server()

if __name__ == '__main__':
    main()