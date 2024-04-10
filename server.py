import random
import socket
import threading
import time
class Server:
    server_ip = '127.0.0.1' 
    server_port = 12345 
    table = [["."]*3 for _ in range(3)]
    whoPlay = 0
    playerWhoWin = 0
    server_socket = any
    client_socket = any
    inputFromClient = ""
    def __init__(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.whoPlay = random.randint(0,1)
        try:
            server_socket.bind((self.server_ip, self.server_port))
            server_socket.listen(5)
            print("Le serveur écoute sur {}:{}".format(self.server_ip, self.server_port))
            self.client_socket, client_address = server_socket.accept()
            print("Connexion entrante de:", client_address)
            self.game()
        except Exception as e:
            print("Une erreur s'est produite lors de l'exécution du serveur:", e)
            
    def listening(self, client_socket):
        data = client_socket.recv(1024)
        if not data:
            print("La connexion avec le client a été fermée.")
            return
        self.inputFromClient = data.decode()
        print("receive : ",self.inputFromClient)
        
    def isNotFinish(self):
        for i in range (0,3):
            if all(element == self.table[i][0] != "." for element in self.table[i]):
                self.playerWhoWin = 0 if self.table[i][0] == "0" else 1
                return False
            
        for j in range(0,3):
            if all(self.table[i][j] == self.table[0][j] != "." for i in range(0,3)):
                self.playerWhoWin = 0 if self.table[0][j] == "0" else 1
                return False
            
        if self.table[1][1] != ".":
            if self.table[0][0] == self.table[1][1] == self.table[2][2] != ".":
                self.playerWhoWin = 0 if self.table[i][0] == "0" else 1
                return False
            if self.table[0][2] == self.table[1][1] == self.table[2][0] != ".":
                self.playerWhoWin = 0 if self.table[i][0] == "0" else 1
                return False
        return True
    
    def isValid(self, selectedLine, selectedRow):
        return selectedLine>=0 and selectedLine<=3 and selectedRow>=0 and selectedRow<=3 and self.table[selectedLine][selectedRow] =="."

    def game(self):
        while self.isNotFinish():
            self.whoPlay = 1 if self.whoPlay == 0 else 0
            if self.whoPlay == 0:
                print(f"C'est au joueur {self.whoPlay} de jouer")
                response = ''.join(''.join(str(element) for element in line) for line in self.table) + "play"
                self.client_socket.sendall(response.encode())
                self.inputFromClient == ""
                while self.inputFromClient == "":
                    client_thread = threading.Thread(target=self.listening, args=(self.client_socket,))
                    client_thread.start()
                self.table[int(self.inputFromClient[0])][int(self.inputFromClient[1])] = "0"
            else:
                print(f"C'est à vous de jouer")
                selectedLine = int(input("Donner la ligne sélectionnée (0,1,2): "))
                selectedRow = int(input("Donner la colonne sélectionnée (0,1,2): "))
                if self.isValid(selectedLine, selectedRow):
                    self.table[selectedLine][selectedRow] = "0" if self.whoPlay == 0 else "X"
                else:
                    while not self.isValid(selectedLine, selectedRow):
                        print(f"C'est à vous de jouer input invalide")
                        selectedLine = int(input("Donner la ligne sélectionnée (0,1,2): "))
                        selectedRow = int(input("Donner la colonne sélectionnée (0,1,2): "))
                    self.table[selectedLine][selectedRow] = "0" if self.whoPlay == 0 else "X"
            print(self.table)
            
        print(f"La partie est finie le joueur {self.playerWhoWin} a gagné")
        if self.playerWhoWin == 0:
            response = ''.join(''.join(str(element) for element in line) for line in self.table)  + "win"
        else:
            response = ''.join(''.join(str(element) for element in line) for line in self.table)  + "loose"
        self.client_socket.sendall(response.encode())
        return
        
if __name__ == "__main__":
    Server()