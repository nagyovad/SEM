# Program keyboardking.py
# Autor: Daniela Nagyová, 8.E <nagyovad@jirovcovka.net>
# Jako základ, jak strukturní tak kódový jsem použila můj minulý úkol reacnidoba.py
# Pro nějaké části jsem použila pomoci AI a poté si ho nechala celý zkontrolovat a uravila jsem chyby
# Hra není úplně dokonalá, dala by se např. přidat podmínka ujišťující se ,že se za jedno kolo přidá jen jeden bod
import tkinter
import tkinter.messagebox
import random

class App(tkinter.Tk):
    def __init__(self, titulek, sirka, vyska):
        super().__init__()
        self.sirka, self.vyska = sirka, vyska
        self.title(titulek)
        self.spravne_skore = 0 # Kolik jsme zmáčkli kláves správně
        self.spatne_skore = 0 # Kolik jsme zmáčkli kláves špatně
        self.pocet_kol = 20 # Na kolik kol se bude hrát
        self.rychlost_kulicky = 250 # Jak rychle padá kulička v prvním kole (čím menší číslo, tím větší rychlost)
        self.klavesy = ["S", "D", "F", "J", "K", "L"]
        self.spravny_obdelnik = None
        self.omezeni_stisku = False
        self.stisknuta_klavesa = False
        
        # Ovládání a popis hry
        self.tlacitko_start = tkinter.Button(self, text="START", command=self.start_hry)
        self.tlacitko_start.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.napis_skore = tkinter.Label(self, text="Skóre: 0:0", font=("Arial", 12, "bold"))
        self.napis_skore.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.platno = tkinter.Canvas(self, width=sirka, height=vyska, background="white")
        self.platno.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.napis_kola = tkinter.Label(self, text="Počet zbývajících kol: 20", font=("Arial", 10))  # Zde jsem změnil na 20
        self.napis_kola.grid(row=2, column=0, columnspan=3, sticky="w", padx=5)

        menubar = tkinter.Menu(self)
        napoveda = tkinter.Menu(menubar, tearoff=0)
        napoveda.add_command(label="O hře", command=self.info_o_hre)
        menubar.add_cascade(label="Nápověda", menu=napoveda)
        menubar.add_command(label="Ukončit", command=self.ukoncit_hru)
        self.config(menu=menubar)

        self.kulicka_spravnosti = self.vytvoreni_kulicky_spravnosti()

       # Vytvoření obdélníků, které představují jednotlivé klávesy
        self.obdelniky = []
        for i, klavesa in enumerate(self.klavesy):
            x0 = 50 + i * 90
            obdelnik = self.platno.create_rectangle(x0, 350, x0 + 60, 380, fill="light gray")
            self.obdelniky.append(obdelnik)

        # Stisknutí kláves
        self.bind("<KeyPress>", self.stisknuti_klavesy)

    def vytvoreni_kulicky_spravnosti(self):
        return self.platno.create_oval(540, 20, 580, 60, fill="light gray")
    
    def start_hry(self): # Vše se musí restartovat pokud je kliknuto na tlačítko START
        self.spravne_skore = 0
        self.spatne_skore = 0
        self.pocet_kol = 20
        self.rychlost_kulicky = 250
        self.napis_skore.config(text="Skóre: 0:0")
        self.napis_kola.config(text="Počet zbývajících kol: 20")
        self.omezeni_stisku = False # Potřebujeme jen jeden stisk za kolo
        self.bind("<KeyPress>", self.stisknuti_klavesy)
        self.nove_kolo()

    def nove_kolo(self):
        self.stisknuta_klavesa = False
        self.omezeni_stisku = False 
        self.pocet_kol = self.pocet_kol - 1
        self.napis_kola.config(text=f"Počet zbývajících kol: {self.pocet_kol}")

        # Zmenšení rychlosti kuličky o 10% pro každé kolo - tedy rychlost kuličky se zvětší
        self.rychlost_kulicky *= 0.90

        if self.spravny_obdelnik:
            self.platno.itemconfig(self.spravny_obdelnik, fill="light gray")
        
        index = random.randint(0, 5)
        self.spravny_obdelnik = self.obdelniky[index]
        self.aktivni_klavesa = self.klavesy[index]
        self.platno.itemconfig(self.spravny_obdelnik, fill="blue")

        x1, _, x2, _ = self.platno.coords(self.spravny_obdelnik)
        stred_x = (x1 + x2) / 2
        self.kulicka = self.platno.create_oval(stred_x - 10, 20, stred_x + 10, 40, fill="red")

        self.padajici_kulicka()

    def padajici_kulicka(self):
        self.platno.move(self.kulicka, 0, 20)
        pozice = self.platno.coords(self.kulicka)
        if pozice[1] < 350:
            self.after(int(self.rychlost_kulicky), self.padajici_kulicka)
        else:
            self.kontrola_konce_kola()

    def kontrola_konce_kola(self):
        if not self.stisknuta_klavesa:
            self.spatne_skore = self.spatne_skore + 1
            self.napis_skore.config(text=f"Skóre: {self.spravne_skore}:{self.spatne_skore}")
        
        self.platno.delete(self.kulicka)
        if self.pocet_kol > 0:
            self.nove_kolo()
        else:
            self.konec_hry()

    def stisknuti_klavesy(self, event):
        if self.pocet_kol <= 0 or self.omezeni_stisku:
            return
        
        if event.keysym.upper() == self.aktivni_klavesa and not self.stisknuta_klavesa:
            self.spravne_skore = self.spravne_skore + 1
            self.napis_skore.config(text=f"Skóre: {self.spravne_skore}:{self.spatne_skore}")
            self.platno.itemconfig(self.kulicka_spravnosti, fill="green")
            self.stisknuta_klavesa = True
        elif not self.stisknuta_klavesa:
            self.spatne_skore = self.spatne_skore + 1
            self.napis_skore.config(text=f"Skóre: {self.spravne_skore}:{self.spatne_skore}")
            self.platno.itemconfig(self.kulicka_spravnosti, fill="red")
            self.omezeni_stisku = True  # Zablokujeme další stisknutí kláves v tomto kole

        self.after(500, self.reset_signal_ball)

    def reset_signal_ball(self):
        self.platno.itemconfig(self.kulicka_spravnosti, fill="light gray")

    def info_o_hre(self):
        okno_o_hre = tkinter.Toplevel(self)
        okno_o_hre.title("O hře")
        tkinter.Label(
            okno_o_hre,
            text="Ve hře se hráč snaží stisknout klávesu která patří k příslušnému rozsvícenému obdelníku. Klávesy jsou z leva: S, D, F, J, K, L. \n"
                 "Každé kolo se obtížnost malinko stěžuje. Hra končí po 20 kolech. Kulička v pravo nahoře indikuje správnost stisku klávesy (zelená-správně, červená-špatně). Hráč se snaží zmáčknout co nevíce kláves správně.",
            font=("Arial", 10)
        ).pack()

    def konec_hry(self):
        tkinter.messagebox.showinfo("Konec hry", f"Tvé skóre je: {self.spravne_skore}:{self.spatne_skore}")
        self.unbind("<KeyPress>")

    def ukoncit_hru(self):
        if tkinter.messagebox.askyesno("Ukončení", "Opravdu chcete ukončit aplikaci?"):
            self.destroy()

    def run(self):  
        self.mainloop()

##### HLAVNÍ PROGRAM
if __name__ == "__main__":
    app = App("Keyboard King", 600, 400)
    # rozběhneme aplikaci
    app.run()
# konec
