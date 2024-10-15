import socket
from threading import Thread
import threading
import sys
import traceback
import json
import argparse


BUFFER = 4096

class RelayServer:
    def __init__(self, host='0.0.0.0', port=6000):
        self.clients = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,  1)
        self.server.bind((host, port))
        self.server.listen()
        self.stop_event = threading.Event()
        

        self.rec_th = Thread(target=self.recieve)
        self.rec_th.start()


    def forward_message(self, message, sender):
        for client in self.clients:
            if client != sender:
                client.sendall(message)

    def handle(self, client, addr):
        while self.stop_event.is_set() != True:
            try:
                message = client.recv(BUFFER)
                if message:
                    self.forward_message(message, client)
              
            except Exception:
                traceback.print_exc()
                self.clients.remove(client)
                break

    def recieve(self):
        while self.stop_event.is_set() != True:
            try:
                client, address = self.server.accept()
                print(f"Client connected  {str(address)}")
                self.clients.append(client)
                Thread(target=self.handle, args=(client,address,)).start()
            except: 
                # traceback.print_exc()
                pass
        print("stop rec_th")
    
    def stop(self):
        print("stop server")
        self.stop_event.set()
        self.server.close()

if __name__ == "__main__":
    server = RelayServer(port=6000)
    # text_server = TextServer(port=6060)
    
    while server.stop_event.is_set() != True:
        inp = input(">")
        match inp:
            case "\help":
                print("<<--------->>")
                print("help message SERVER")
                print(f"current VOICE SERVER 0.0.0.0:6000")
                print(f"current TEXT SERVER 0.0.0.0:6060")
                print("\close for disconnect")
                print("<<--------->>")
            case "\close":
                server.stop()
                # text_server.stop()
                sys.exit(0)
