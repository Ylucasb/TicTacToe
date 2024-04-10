import socket
import threading

class client:
    table = list()
    server_ip = '127.0.0.1' 
    server_port = 12345 
    client_socket = any
    responseFromServer = ""
    win = False
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print("Connexion établie avec le serveur.")
            server_thread = threading.Thread(target=self.receive_from_server, args=(self.client_socket,))
            server_thread.start()
        except Exception as e:
            print("Une erreur s'est produite lors de la connexion au serveur:", e)
            
    def receive_from_server(self, server_socket):
        while True:
            try:
                data = server_socket.recv(1024)
                if not data:
                    print("La connexion avec le serveur a été fermée.")
                    return 
                self.responseFromServer = data.decode()
                if self.responseFromServer != "":
                    self.restoreTable(self.responseFromServer[:9])
                    self.display()
                    message = self.responseFromServer[9:]
                    if message == "play":
                        print(f"C'est à vous de jouer")
                        selectedLine = int(input("Donner la ligne sélectionnée (0,1,2): "))
                        selectedRow = int(input("Donner la colonne sélectionnée (0,1,2): "))
                        if self.isValid(selectedLine, selectedRow):  
                            message = str(selectedLine) + str(selectedRow)
                            self.client_socket.sendall(message.encode())
                        else:
                            while not self.isValid(selectedLine, selectedRow):
                                print(f"C'est à vous de jouer input invalide")
                                selectedLine = int(input("Donner la ligne sélectionnée (0,1,2): "))
                                selectedRow = int(input("Donner la colonne sélectionnée (0,1,2): "))
                            message = str(selectedLine) + str(selectedRow)
                            self.client_socket.sendall(message.encode())
                    elif message == "loose":
                        print("Vous avez perdu")
                        break
                    elif message == "win":
                        print("Vous avez gagné")
                        break
                    else:
                        print("error :", message)
            except Exception as e:
                print("Une erreur s'est produite lors de la réception des données du serveur:", e)
                return
            
    def isValid(self, selectedLine, selectedRow):
        return selectedLine>=0 and selectedLine<=3 and selectedRow>=0 and selectedRow<=3 and self.table[selectedLine][selectedRow] =="."
    
    def display(self):
        print(self.table[0][0], " | ", self.table[0][1], " | ",self.table[0][2])
        print("--------------")
        print(self.table[1][0], " | ", self.table[1][1], " | ",self.table[1][2])
        print("--------------")
        print(self.table[2][0], " | ", self.table[2][1], " | ",self.table[2][2])
        print("--------------")
        
    def restoreTable(self, encodedTable):
        line = list()
        self.table = list()
        i = 0
        for element in encodedTable:
            i +=1
            line.append(element)
            if i == 3:
                self.table.append(line)
                line = []
                i = 0
                
if __name__ == "__main__":
    client()
