import socket
import ssl
import threading

HOST = "127.0.0.1"
PORT = 60000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="secrets/certificate.pem", keyfile="secrets/key.pem")

# Wrap the socket with SSL
server = context.wrap_socket(server, server_side=True)


if __name__ == "__main__":
    server.bind((HOST, PORT))
    server.listen(5)

    while True:
        connection, client_address = server.accept()
        print(f"Connection from {client_address}")

        def handle_client(conn):
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode('utf-8')}")
            conn.close()

        threading.Thread(target=handle_client, args=(connection,)).start()