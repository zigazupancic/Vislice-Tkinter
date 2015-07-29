__author__ = 'Žiga Zupančič'

from tkinter import *
from tkinter import messagebox
import random
import os

class Vislice():
    def __init__(self, master):

        self.master = master

        #Glavni meni
        menu = Menu(master)
        master.config(menu=menu)

        #Podmeni Datoteka
        file_menu = Menu(menu)
        menu.add_cascade(label="Datoteka", menu = file_menu)

        #Podmeni Pomoč
        help_menu = Menu(menu)
        menu.add_cascade(label="Pomoč", menu = help_menu)

        #Vsebina podmenija Datoteka
        file_menu.add_command(label = "Nova igra", command = self.igra)
        file_menu.add_command(label = "Odpri igro", command = self.odpri)
        file_menu.add_command(label = "Shrani igro", command = self.shrani)
        file_menu.add_separator()
        file_menu.add_command(label = "Izhod", command = master.destroy)

        #Vsebina podmenija Pomoč
        help_menu.add_command(label = "Kako igrati", command = self.kako_igrati)
        help_menu.add_command(label = "O programu", command = self.o_programu)

        
        self.igra()

    def kako_igrati(self):
        os.startfile("kako_igrati.txt")

    def o_programu(self):
        os.startfile("o_programu.txt")

    def ponastavitev(self):
        master = self.master
        #Postavitev okvirja za risanje vislic
        self.vislice = Canvas(master, width = 350, height = 400)
        self.vislice.grid(row = 4, column = 2)
        #Izris okvirja
        self.vislice.create_rectangle(4, 4, 350, 400, width = 4)

        #Postavitev praznih črtic za ugibanje besed
        self.crtice = Canvas(master, width = 600, height = 150)
        self.crtice.grid(row = 3, column = 2)

        #Polje za napis napačnih črk
        self.polje_napacnih = Canvas(master, width = 400, height = 400)
        self.polje_napacnih.grid(row = 4, column = 3)
        self.polje_napacnih.create_rectangle(4, 4, 400, 400, width = 4, outline = "red") #Obroba
        self.polje_napacnih.create_text(200, 30, text = "Napačne črke:", font = ('Helvetica', '30', 'bold'), fill = "red")

        #Polje za vnos črk in potrditvena tipka
        vnesi_crko = Label(text = " Ugibaj črko: ")
        vnesi_crko.grid(row = 0, column = 0)
        self.crka = StringVar(master, value = None)
        vnos = Entry(master, textvariable = self.crka)
        vnos.grid(row = 1, column = 0)
        vnos.focus() #vnosno polje je fokusirano in pripravljeno za pisanje
        potrdi = Button(master, text = "  Ugibaj  ", command = self.ugibaj)
        potrdi.grid(row = 1, column = 1, rowspan = 2)
        root.bind('<Return>', self.ugibaj) #Potrjevanje črke z uporabo tike <Return>


    def ugibaj(self, event = None):
        #argument event = None dodan zaradi bind()
        #Preveri, če je vnešen znak le en in če je črka slovenske abecede
        #Če je, preveri, ali je pravilen, ali ne in ga razvrsti v ustrezen seznam
        if len(self.crka.get()) == 1 and (self.crka.get()) in "abcčdefghijklmnoprsštuvzž":
            if self.crka.get() in self.beseda:
                if self.crka.get() not in self.uganjene:
                    self.uganjene.append(self.crka.get())
                    for i, znak in enumerate(self.crke_besede):
                        if znak in self.uganjene:
                            self.pravilna_crka(i, znak)
            else:
                if self.crka.get() not in self.napacne:
                    self.napacne.append(self.crka.get())
                    self.neuspeli_poskusi += 1
                    self.napacna_crka(self.neuspeli_poskusi, self.crka.get())
                    self.izris_vislic(self.neuspeli_poskusi)

        #Vnosno polje naredi prazno
        self.crka.set("")

        #Konča igro, če uganeš besedo ali če izgubiš
        if set(self.uganjene) == set(self.crke_besede):
            self.konec_igre(True)

        elif self.neuspeli_poskusi >= 8:
            self.konec_igre(False)

    #Ob koncu igre
    def konec_igre(self, zmaga):
        if zmaga:
            messagebox.showinfo("Konec igre", "Zmagali ste!")
        else:
            messagebox.showinfo("Konec igre", "Izgubili ste!")
            messagebox.showinfo("Beseda", "Beseda, ki je niste uganili je: " + self.beseda + ".")

        #Vprašanje za novo igro
        nova_igra = messagebox.askyesno("Nova igra", "Ali želite igrati novo igro?")
        if nova_igra == True:
            self.igra()
        else:
            root.destroy()


    def izris_vislic(self, stopnja):
        #Izbira barve za palice
        barva = "#EDAB55"

        #Izris podlage
        if stopnja == 1:
            self.vislice.create_rectangle(25, 350, 325, 390, fill = barva, outline=barva)
        #Izris pokoncne palice
        if stopnja == 2:
            self.vislice.create_line(100, 350, 100, 50, width = 10, fill = barva)
        #Izris opore za pokoncno palico
        if stopnja == 2:
            self.vislice.create_line(50, 360, 100, 310, width = 8, fill = barva)
            self.vislice.create_line(150, 360, 100, 310, width = 8, fill = barva)
        #Izris prečne palice
        if stopnja == 3:
            self.vislice.create_line(95, 50, 230, 50, width = 10, fill = barva)
        #Izris opore za prečno palico
        if stopnja == 3:
            self.vislice.create_line(100, 100, 150, 50, width = 8, fill = barva)
        #Izris vrvi
        if stopnja == 4:
            self.vislice.create_line(226, 50, 226, 100, width = 8, fill = barva)
        #Izris glave
        if stopnja == 5:
            self.vislice.create_oval(200, 100, 252, 152)
        #Izris teles
        if stopnja == 5:
            self.vislice.create_line(226, 152, 226, 240)
        #Izris leve noge
        if stopnja == 6:
            self.vislice.create_line(226, 240, 190, 290)
            self.vislice.create_line(190, 290, 175, 280)
        #Izris desne noge
        if stopnja == 6:
            self.vislice.create_line(226, 240, 262, 290)
            self.vislice.create_line(262, 290, 277, 280)
        #Izris leve roke
        if stopnja == 7:
            self.vislice.create_line(226, 190, 180, 150)
        #Izris desne roke
        if stopnja == 7:
            self.vislice.create_line(226, 190, 272, 150)
        #Izris obraza
        if stopnja == 8:
            self.vislice.create_line(208,115,218,125)
            self.vislice.create_line(208,125,218,115)
            self.vislice.create_line(234,125,244,115)
            self.vislice.create_line(234,115,244,125)
            self.vislice.create_line(213,140,239,140)

    def izris_crtic(self, stevilo):
        for i in range(stevilo):
            self.crtice.create_line(40 + i*50, 100, 80 + i*50, 100)

    def pravilna_crka(self, pozicija, crka):
        crka = crka.upper()
        self.crtice.create_text(60 + pozicija*50, 80, text = crka, font = ('Helvetica', '30', 'bold'))

    def napacna_crka(self, pozicija, crka):
        crka = crka.upper()
        if pozicija <= 6:
            vrsta = 1
        elif pozicija <= 12:
            vrsta = 2
            pozicija = pozicija - 6
        elif pozicija <= 18:
            vrsta = 3
            pozicija = pozicija - 12
        self.polje_napacnih.create_text(pozicija*60, 20 + 70*vrsta, text = crka, font = ('Helvetica', '30', 'bold'))

    def igra(self):
        self.ponastavitev() #ponastavi igralno površino
        self.seznam_besed = []

        #iz datoteke z besedami izbere naključno za igro
        with open("seznam_besed.txt") as file:
            for beseda in file:
                self.seznam_besed.append(beseda.rstrip())
        self.beseda = random.choice(self.seznam_besed)

        #ponastavi spremenljivke
        self.neuspeli_poskusi = 0
        self.crke_besede = list(self.beseda.lower())
        self.uganjene = []
        self.napacne = []
        self.uganjene.append(random.choice(self.crke_besede))
        self.izris_crtic(len(self.crke_besede))

        for i, znak in enumerate(self.crke_besede):
            if znak in self.uganjene:
                self.pravilna_crka(i, znak)


    def odpri(self):
        with open("shranjena_igra.txt", encoding="Utf-8") as file:
            podatki = file.readlines()
        for i, podatek in enumerate(podatki):
            if i == 0:
                self.beseda = self.seznam_besed[int(podatek.rstrip())]
            elif i == 1:
                podatek = podatek.rstrip()
                self.uganjene = podatek.split(";")
            elif i == 2:
                podatek = podatek.rstrip()
                self.napacne = podatek.split(";")
            elif i == 3:
                self.neuspeli_poskusi = int(podatek.rstrip())
        self.ponastavitev()
        self.crke_besede = list(self.beseda.lower())
        self.izris_crtic(len(self.crke_besede))

        for i, znak in enumerate(self.crke_besede):
            if znak in self.uganjene:
                self.pravilna_crka(i, znak)

        for i, znak in enumerate(self.napacne):
            self.napacna_crka(i+1, znak)

        for i in range(self.neuspeli_poskusi):
            self.izris_vislic(i+1)
        messagebox.showinfo("Odpri", "Igra odprta!")


    def shrani(self):
        with open("shranjena_igra.txt", 'wt', encoding="Utf-8") as file:
            file.write(str(self.seznam_besed.index(self.beseda))+"\n")
            file.write(';'.join(self.uganjene) + "\n")
            file.write(';'.join(self.napacne) + "\n")
            file.write(str(self.neuspeli_poskusi))
        messagebox.showinfo("Shrani", "Uspešno shranjeno!")

root = Tk()
root.wm_title("Vislice")
aplikacija = Vislice(root)

root.mainloop()
