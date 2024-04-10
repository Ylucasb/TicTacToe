import random
class Server:
    table = [["."]*3 for _ in range(3)]
    whoPlay = 0
    playerWhoWin = 0
    def __init__(self):
        self.whoPlay = random.randint(0,1)
        self.game()
    def game(self):
        while self.isNotFinish():
            self.whoPlay = 1 if self.whoPlay == 0 else 0
            print(f"C'est au joueur n°{self.whoPlay} de jouer")
            selectedLine = int(input("Donner la ligne sélectionnée (0,1,2): "))
            selectedRow = int(input("Donner la colonne sélectionnée (0,1,2): "))
            if self.isValid(selectedLine, selectedRow):
                self.table[selectedLine][selectedRow] = "0" if self.whoPlay == 0 else "X"
            else:
                while not self.isValid(selectedLine, selectedRow):
                    print(f"Numéro invalide")
                    selectedLine = int(input("Donner la ligne sélectionnée (0,1,2): "))
                    selectedRow = int(input("Donner la colonne sélectionnée (0,1,2): "))
                self.table[selectedLine][selectedRow] = "0" if self.whoPlay == 0 else "X"
            print(self.table)
        print(f"La partie est finie le joueur {self.playerWhoWin} a gagné")
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

if __name__ == "__main__":
    server = Server()