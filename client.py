import socket
import os

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 60577))
print("Sunucuya bağlandı... (Çıkmak için 'exit' yazın)...")


def send_file(filename):
    if not os.path.exists(filename):
        print(f"Hata: {filename} dosyası bulunamadı.")
        return False

    file_size = os.path.getsize(filename)
    client_socket.send(f"FILE:{os.path.basename(filename)}:{file_size}".encode())

    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            client_socket.send(data)
    client_socket.send(b"ENDFILE")
    return True


def show_options():
    print("\n--- İşlem Seçenekleri ---")
    print("Mesaj göndermek için 'm'")
    print("Dosya göndermek için 'd'")
    print("Çıkmak için 'exit'")
    return input("Seçiminiz: ").lower()


while True:
    choice = show_options()

    if choice == 'm':
        message = input("Client: ")
        client_socket.send(f"MSG:{message}".encode())

        if message.lower() == "exit":
            print("Oturum sonlandırıldı.")
            break

        response = client_socket.recv(1024).decode()
        print(f"Sunucudan gelen cevap: {response}")

        if response.lower() == "exit":
            print("Sunucu oturumu sonlandırdı.")
            break

    elif choice == 'd':
        file_path = input("Dosya yolunu girin: ")
        if send_file(file_path):
            print(f"{file_path} dosyası gönderildi.")

            response = client_socket.recv(1024).decode()
            print(f"Sunucudan gelen cevap: {response}")

    elif choice == 'exit':
        print("Oturum sonlandırıldı.")
        client_socket.send("EXIT:".encode())
        break

    else:
        print("Geçersiz seçim. Lütfen tekrar deneyin.")

client_socket.close()