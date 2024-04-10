import socket
import threading

def receive_from_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("La connexion avec le client a été fermée.")
                break
            print("\nMessage du client:", data.decode())
            print("Entrez votre réponse (ou 'exit' pour quitter) : ")
        except Exception as e:
            print("Une erreur s'est produite lors de la réception des données du client:", e)
            break

def main():
    server_ip = '127.0.0.1' 
    server_port = 12345 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(5)
        print("Le serveur écoute sur {}:{}".format(server_ip, server_port))
        client_socket, client_address = server_socket.accept()
        print("Connexion entrante de:", client_address)
        client_thread = threading.Thread(target=receive_from_client, args=(client_socket,))
        client_thread.start()

        while True:
            response = input("Entrez votre réponse (ou 'exit' pour quitter) : ")
            client_socket.sendall(response.encode())
            if response.lower() == 'exit':
                break

    except Exception as e:
        print("Une erreur s'est produite lors de l'exécution du serveur:", e)

    finally:
        if client_socket:
            client_socket.close()
        if server_socket:
            server_socket.close()

if __name__ == "__main__":
    main()
