# slovnik.py
# Program: ukázka práce s databází SQLite v OOP
# Author: 
# Date: 

### modul pro práci s SQLite
import sqlite3

# třída pro práci s databází
class SQLite(object):
    ### konstruktor
    def __init__(self, filename):
        self.filename = filename
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()
    ### metoda pro zaslání SQL dotazu    
    def sql(self, query, data=None):
        '''
         generické vložení do SQLite databaze s commitem
        '''    
        if data == None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)
        self.connection.commit()
        return self.cursor
    ### destruktor
    def __del__(self):
        '''
          magická metoda, která se volá před  smazáním objektu
          v našem případě před smazáním uzavřeme spojení na databázi
        '''    
        self.connection.close()
# třída pro práci se slovníkem        
class DBslovicka(SQLite):
    ### konstruktor
    def __init__(self, filename):
        super().__init__(filename)
        # vytvoření tabulky, pokud neexistuje
        self.sql("""CREATE TABLE IF NOT EXISTS slovicka
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ang TEXT NOT NULL,
                 cz TEXT NOT NULL) """)
    ### metoda pro uložení slovíčka
    def ulozslovicko(self, cz, ang):
        self.sql("INSERT INTO slovicka (cz,ang) VALUES (?,?);", (cz,ang))
        return None
    ### metoda pro získání seznamu slovíček    
    def seznamslovicek(self):
        data = self.sql("SELECT cz, ang FROM slovicka;")
        seznam = data.fetchall()
        return seznam
    ### metoda pro hledání slovíčka
    def hledejslovicko(self, slovicko, lang="en"):
        if lang == "en":
            kursor = self.sql("SELECT ang, cz FROM slovicka WHERE ang=?", (slovicko,))
        elif lang == "cz":
            kursor = self.sql("SELECT ang, cz FROM slovicka WHERE cz=?", (slovicko,))
        else:
            return None
        return kursor.fetchone()
# třída pro práci s aplikací   
class Aplikace(object):
    # konstruktor
    def __init__(self, dbfile):
        self.db = DBslovicka(dbfile)
    # metoda pro zobrazení menu    
    def menu(self):
        povolene = ["k", "z", "v", "s", "q"]
        volba = ""
        print("--------SLOVNIK---------")
        print("    z ... zadání slovíčka CZ-ANG")
        print("    v ... zobraz všechna slovíčka")
        print("    s ... hledej ANG (překlad do CZ)")
        print("    k ... konec")
        print("---------------------")
        # získání volby od uživatele v cyklu
        while volba.lower() not in povolene:  
            volba = input("Zadej svou volbu: ")
        return volba.lower() 
    # metoda pro zobrazení slovíček    
    def zobraz(self):
        print("-----------------------------------------------------")
        for cz,ang in self.db.seznamslovicek():
            print(f"{cz:20} {ang:20}")
        print("-----------------------------------------------------")
    # metoda pro zadání slovíčka    
    def zadejslovicko(self):
        cz = input("Zadej české slovo: ")
        ang = input("Zadej příslušné anglické slovo: ")
        self.db.ulozslovicko(cz,ang)
        self.zobraz()
    # metoda pro hledání slovíčka    
    def hledejslovicko(self):
        ang = input("Zadej anglické slovo: ")
        vysledek = self.db.hledejslovicko(ang)
        if vysledek == None:
            print(f"Slovíčko {ang} nebylo nalezeno ve slovníku!!!")
        else:
            en, cz = vysledek
            print(f"{ang} => {cz}")
    def run(self):
        while True:
            volba = self.menu()
            if (volba == "k" or volba == "q"):
                break
            elif (volba == "z"):
                self.zadejslovicko()
            elif (volba == "s"):
                self.hledejslovicko()
            elif (volba == "v"):
                self.zobraz()
########## Hlavní program
if __name__ == "__main__":
    app = Aplikace("slovnik.db")
    # start hlavní programové smyčky
    app.run()
    print("Bye")
########## KONEC programu 