import random
import socket
import ssl
import threading
import argparse
from time import sleep

from tls_server import HOST as SERVER_HOST
from tls_server import PORT as SERVER_PORT

HOST = "127.0.0.1"
PORT = 60001

def create_client(client_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(keyfile="secrets/key.pem", certfile="secrets/certificate.pem")

    # Disable hostname verification, correct fix for production would be to keep file with trusted certificates
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    client = context.wrap_socket(client, server_hostname=SERVER_HOST)

    client.bind((HOST, PORT + client_id))
    client.connect((SERVER_HOST, SERVER_PORT))

    return client

def setup_secret_sharing(private_input):
    share1, share2 = random.randint(0, 100), random.randint(0, 100)
    sum = share1 + share2
    share3 = private_input - sum
    return share1, share2, share3

def something(client_id):
    private_input = random.randint(0, 100)
    share1, share2, share3 = setup_secret_sharing(private_input)
    print(f"Client {client_id} shares: {share1}, {share2}, {share3}")

    client = create_client(client_id)
    client.send(f"{share1},{share2},{share3}".encode("utf-8"))

    response = client.recv(1024)
    print(f"Client {client_id} received: {response.decode('utf-8')}")

    client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TLS Client")
    parser.add_argument("client_id", type=int, help="ID of the client")
    args = parser.parse_args()

    client_id = args.client_id
    # client = create_client(client_id)
    
    something(client_id)