# Program: nakupy.py
# Author: Nagyová Daniela

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
        magická metoda, která se volá před smazáním objektu
        v našem případě před smazáním uzavřeme spojení na databázi
        '''    
        self.connection.close()
# třída pro práci s nákupním seznamem
class nakupni_seznam(SQLite):
    ### konstruktor
    def __init__(self, filename):
        super().__init__(filename)
        # vytvoření tabulky, pokud neexistuje
        self.sql("""CREATE TABLE IF NOT EXISTS nakupy
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 co TEXT NOT NULL,
                 kolik REAL NOT NULL,
                 jcena REAL NOT NULL,
                 poznamka CHAR(80))""")
    ### metoda pro přidání zboží do nákupního seznamu
    def pridej_polozku(self, co, kolik, jcena, poznamka=""):
        self.sql("INSERT INTO nakupy (co, kolik, jcena, poznamka) VALUES (?, ?, ?, ?);", (co, kolik, jcena, poznamka))
        return None
    ### metoda pro zobrazení zboží z nákupního seznamu
    def seznam_polozek(self):
        data = self.sql("SELECT * FROM nakupy;")
        seznam = data.fetchall()
        return seznam
    
# třída pro práci s aplikací 
class Aplikace(object):
    # konstruktor
    def __init__(self, dbfile):
        self.db = nakupni_seznam(dbfile)
    # metoda pro zobrazení menu 
    def menu(self):
        povolene = ["z", "p", "k"]
        volba = ""
        print("-------- NÁKUPNÍ LÍSTEK --------")
        print("    z ... zobrazit nákupní seznam")
        print("    p ... přidat položku")
        print("    k ... konec")
        print("---------------------------------")
        # získání volby od uživatele v cyklu
        while volba.lower() not in povolene:  
            volba = input("Zadejte volbu [z/p/k]: ")
        return volba.lower()
    
    # metoda pro zobrazení nákupního seznamu  
    def zobraz_polozky(self):
        print("\n-------- Seznam nákupů --------")
        for id, co, kolik, jcena, poznamka in self.db.seznam_polozek():
            print(f"id: {id}, co: {co}, kolik: {kolik}, cena: {jcena}, poznámka: {poznamka}")
        print("--------------------------------\n")
    # metoda pro přidání položky do nákupního seznamu   
    def pridej_polozku(self):
        co = input("Zadejte název zboží: ")
        kolik = float(input("Zadejte počet kusů: "))
        jcena = float(input("Zadejte jednotkovou cenu: "))
        poznamka = input("Zadejte poznámku: ")
        self.db.pridej_polozku(co, kolik, jcena, poznamka)
        self.zobraz_polozky()

    def run(self):
        while True:
            volba = self.menu()
            if (volba == 'k'):
                break
            elif (volba == 'z'):
                self.zobraz_polozky()
            elif (volba == 'p'):
                self.pridej_polozku()
            else:
                print("Nenalezeno, nevadí zkus to znova.\n")

########## Hlavní program
if __name__ == "__main__":
    app = Aplikace("nakupy.db")
    # start hlavní programové smyčky
    app.run()
    print("Bye")
########## KONEC programu 
