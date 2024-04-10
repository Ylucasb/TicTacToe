import socket
import threading

def receive_from_server(server_socket):
    while True:
        try:
            data = server_socket.recv(1024)
            if not data:
                print("La connexion avec le serveur a été fermée.")
                break
            print("\nMessage du serveur:", data.decode())
            print("Entrez votre réponse (ou 'exit' pour quitter) : ")
        except Exception as e:
            print("Une erreur s'est produite lors de la réception des données du serveur:", e)
            break

def main():
    server_ip = '127.0.0.1' 
    server_port = 12345 

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
        print("Connexion établie avec le serveur.")
        server_thread = threading.Thread(target=receive_from_server, args=(client_socket,))
        server_thread.start()

        while True:
            message = input("Entrez votre message ('exit' pour quitter) : ")
            client_socket.sendall(message.encode())
            if message.lower() == 'exit':
                break

    except Exception as e:
        print("Une erreur s'est produite lors de la connexion au serveur:", e)

    finally:
        if client_socket:
            client_socket.close()

if __name__ == "__main__":
    main()
