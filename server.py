import socket
import os


def receive_file(client_socket, filename):
    safe_filename = os.path.basename(filename)
    safe_filename = os.path.join('received_files', safe_filename)

    os.makedirs('received_files', exist_ok=True)

    with open(safe_filename, 'wb') as f:
        while True:
            data = client_socket.recv(1024)
            if data.endswith(b"ENDFILE"):
                f.write(data[:-7])
                break
            f.write(data)
    print(f"{safe_filename} dosyası başarıyla alındı")
    return safe_filename


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = "localhost"
PORT = 60577
server_address = (HOST, PORT)
server_socket.bind(server_address)
server_socket.listen(5)
print(f"Server {HOST}:{PORT} adresinde dinliyor...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Server {client_address} adresine bağlandı")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        message = data.decode()

        if message.startswith("EXIT:"):
            print("Client oturumu sonlandırdı...")
            client_socket.close()
            break
        elif message.startswith("FILE:"):
            _, filename, _ = message.split(":")
            received_filename = receive_file(client_socket, filename)
            client_socket.send(f"{received_filename} dosyası başarıyla alındı".encode())
        elif message.startswith("MSG:"):
            print(f"Alınan mesaj: {message[4:]}")
            s_message = input("Server: ")
            client_socket.send(s_message.encode())
        else:
            print(f"Beklenmeyen mesaj: {message}")

    if message.startswith("EXIT:"):
        break

server_socket.close()