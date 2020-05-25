import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  # per includere oggetto e allegato bisogna usare il modulo MIMEMultipart
from email.mime.base import MIMEBase  # MIMEBase serve per codificare il file da usare come allegato
from email import encoders  # encoders trasforma l'allegato in base64


indirizzi = []
file = "Risorse/testo/testo.txt"


# FUNZIONE GESTIONE DELLA SCHERMATA DI LOGIN E CREDENZIALI
def login():

    if username.get() == "paektusan2020@gmail.com" and password.get() == "Baresi2020!":

        root.destroy()
        gestione(username, password)

    else:

        errato = Label(root, text="Username o Password errate")
        errato.place(x=70, y=170)


# RIEMPIO UNA LISTA CON TUTTI GLI INDIRIZZI EMAIL
def riempiLista():

    indirizzi.clear()  # ogni volta la svuoto per evitare doppioni
    try:

        f = open(file, "r+")
        line = f.readline().strip()

        while line != '':
            mail = line
            line = f.readline().strip()
            indirizzi.append(mail)

        f.close()

    except IOError:
        print("Errore nel file da input\n")
    except ():
        print("Unexpected error:", sys.exc_info()[0])
        raise


# FUNZIONE PER RICERCARE LA MAIL NELLA LISTA E VERIFICARNE LA PRESENZA
def ricercaAggiunta(labelPresente, name):

    riempiLista()  # devo richiamarlo per fare in modo che la lista sia sempre aggiornata
    if name.get() == "":  # evito la possibilità che venga inserita una stringa vuota nel file

        labelPresente.config(text="Inserisci un nome")

    else:

        for i in indirizzi:
            if name.get() == i:  # se trovo la mail

                labelPresente.config(text="Email presente")
                return

        mailAssente(labelPresente, name)  # se non la trovo


# FUNZIONE NEL CASO LA MAIL NON VENGA TROVATA PER AGGIUNGERLA
def mailAssente(labelPresente, name):

    # creo una nuova finestra con un label e due pulsanti, se scelgo di non aggiungere la chiudo, altrimenti v. aggiunta
    labelPresente.config(text="Email assente")

    window2 = Tk()
    window2.minsize(100,50)
    window2.geometry("+550+300")
    window2.title("Conferma aggiunta")

    confermaAggiunta = Label(window2, text="Confermi di voler aggiungere l'indirizzo alla lista?").grid(column=0, row=0)
    # uso una lambda function per poter passare argomenti, che non si potrebbe fare nella dichiarazione di un button
    si = ttk.Button(window2, text="Sì", command=lambda: aggiunta(window2, labelPresente, name)).grid(column=0, row=1)
    no = ttk.Button(window2, text="No", command=window2.destroy).grid(column=0, row=2)


# FUNZIONE CHE GESTISCE IL CASO IN CUI VENGA PREMUTO IL TASTO SI PER AGGIUNGERE
def aggiunta(window2, labelPresente, name):

    # altrimenti vado ad aggiungere scrivendo la mail nel file, chiudo la finestra e stampo il risultato su label
    fd = open("Risorse/testo/testo.txt", "a")
    fd.write("\n" + name.get())
    fd.close()
    window2.destroy()
    labelPresente.config(text="Email aggiunta correttamente")


# FUNZIONE PER LA GESTIONE DEL PULSANTE ALLEGA FILE
def allega(labelFileScelto):

    allega.has_been_called_allega = True  # se sono entrato in questa mail lo setto a true
    global percorso_allegato
    percorso_allegato = filedialog.askopenfilename()  # variabile che contiene il percorso per l'allegato alla mail
    global path
    path = Path(percorso_allegato)  # Passo l'output di askopenfilename() che sarebbe l'intero path per arrivare al file
    labelFileScelto.config(text="Allegato il file: " + path.name)  # attraverso Path stampo solo il nome


allega.has_been_called_allega = False  # altrimenti va a False di default


# FUNZIONE PER LA GESTIONE DELL'OGGETTO
def oggettoEmail(window, oggettomail):

    confermaOggetto = Label(window, text="")

    if oggettomail.get() == "":

        confermaOggetto.config(text="Inserire un oggetto")
        confermaOggetto.place(x=380, y=68)

    else:

        confermaOggetto.config(text="Oggetto caricato correttamente")
        confermaOggetto.place(x=380, y=68)


# FUNZIONE PER LA GESTIONE DEL TESTO
def testoEmail(window, testoEntry):

    testoEmail.has_been_called_testo = True  # se sono entrato in questa mail lo setto a true
    global inputTesto
    inputTesto = testoEntry.get("1.0", "end-1c")  # idk pls send documentation
    confermaTesto = Label(window, text="")

    if inputTesto == "":

        confermaTesto.config(text="Inserire un testo")
        confermaTesto.place(x=380, y=213)

    else:

        confermaTesto.config(text="Testo caricato correttamente")
        confermaTesto.place(x=380, y=213)


testoEmail.has_been_called_testo = False  # altrimenti va a False di default


# FUNZIONE PER INVIARE CREARE LA FINESTRA PER LA VERIFICA DI INVIO
def verificaInvioNewsletter(window, oggettomail, username, password):

    # controllo di essere entrato nelle funzioni per definire il testo e l'allegato
    if testoEmail.has_been_called_testo is True and allega.has_been_called_allega is True:

        # controllo che l'oggetto sia stato definito
        if oggettomail.get() != "":

            # creo una finestra di conferma invio
            finestra_invio = tk.Tk()
            finestra_invio.title("Conferma invio")
            finestra_invio.minsize(330, 20)
            finestra_invio.geometry("+550+300")
            labelAvviso = Label(finestra_invio, text="Procedere con l'invio della newsletter?")
            labelAvviso.place(x=40, y=60)
            bottoneInvio = ttk.Button(finestra_invio, text="Invia", command=lambda: inviaNewsletter(finestra_invio, oggettomail, username, password))
            bottoneInvio.place(x=80, y=100)
            bottoneAnnulla = ttk.Button(finestra_invio, text="Annulla", command=finestra_invio.destroy)
            bottoneAnnulla.place(x=165, y=100)

    else:

        labelInvio = Label(window, text="Inserire tutti i dati")
        labelInvio.place(x=415, y=315)


# FUNZIONE PER INVIARE LA NEWSLETTER
def inviaNewsletter(finestra_invio, oggettomail, username, password):

    riempiLista()
    for i in indirizzi:

        email_user = username.get()
        oggetto = oggettomail.get()

        msg = MIMEMultipart()  # creo un oggetto multiparte
        msg['From'] = email_user
        msg['To'] = i
        msg['Subject'] = oggetto

        contenuto = inputTesto
        msg.attach(MIMEText(contenuto, 'plain'))  # ci attacco per primo il testo della mail

        filename = percorso_allegato
        allegato = open(filename, 'rb')
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(allegato.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename = " + path.name)
        msg.attach(p)  # dopo averlo aperto e codificato ci attacco l'allegato

        testo = msg.as_string()  # lo rendo una stringa

        mail = smtplib.SMTP('smtp.gmail.com', 587)  # mi attacco ai server

        mail.starttls()  # comincio la starttls per rendere la mia connessione crittografata
        mail.ehlo()  # mi identifico

        mail.login(email_user, password.get())  # faccio il login

        mail.sendmail(email_user, i, testo)  # invio ad ogni elemento della lista una mail

        mail.close()

    finestra_invio.destroy()


# CREO LA FINESTRA DI LOGIN
root = tk.Tk()
root.title("Login")
root.minsize(330, 30)
root.geometry("+550+300")

# LOAD E RENDER DELL'IMMAGINE
img = PhotoImage(file="Risorse/png/paek.png")
img = img.zoom(10)
img = img.subsample(15)
panel = Label(root, image=img)
panel.place(x=90, y=0)

# DICHIARAZIONI CREDENZIALI DI LOGIN
labelUsername = Label(root, text="Username:")
labelPassword = Label(root, text="Password:")
username = StringVar()
password = StringVar()
usernameEntered = Entry(root, width=25, textvariable=username)
passwordEntered = Entry(root, show="*", width=25, textvariable=password)
conferma = ttk.Button(root, text="Login", command=lambda: login())

# POSIZIONI CREDENZIALI DI LOGIN
labelUsername.place(x=0, y=60)
labelPassword.place(x=0, y=90)
usernameEntered.place(x=80, y=60)
passwordEntered.place(x=80, y=90)
conferma.place(x=120, y=140)


# FUNZIONE CHE CONTIENE LA FINESTRA PRINCIPALE
def gestione(username, password):

    # CREO LA FINESTRA DI GESTIONE
    window = tk.Tk()
    window.title("Gestione")
    window.minsize(630, 450)
    window.geometry("+400+250")

    img1 = PhotoImage(file="Risorse/png/paekWindow.png")
    panel1 = Label(window, image=img1)
    panel1.place(x=125, y=0)

    # DICHIARAZIONI AGGIUNTA DI UNA MAIL
    labelInserimento = Label(window, text="Inserisci una mail per aggiungerla agli iscritti")
    mailIscritto = StringVar()
    mailInserita = Entry(window, width=25, textvariable=mailIscritto)  # text box per l'input di def grep
    labelPresente = Label(window)  # questo label serve per controllare la presenza della mail v. def grep
    ricerca = ttk.Button(window, text="Aggiungi mail", command=lambda: ricercaAggiunta(labelPresente, mailIscritto))

    # DICHIARAZIONI ALLEGA FILE
    labelAllegato = Label(window, text="Allegato Mail")
    labelFileScelto = Label(window)
    allegato = ttk.Button(window, text="Allega file", command=lambda: allega(labelFileScelto))

    # DICHIARAZIONI ALLEGA OGGETTO
    labelOggetto = Label(window, text="Oggetto Mail")
    oggettoMail = StringVar()
    oggettoEntry = Entry(window, width=25, textvariable=oggettoMail)
    oggettoInvio = ttk.Button(window, text="Invio", command=lambda: oggettoEmail(window, oggettoMail))

    # DICHIARAZIONI ALLEGA TESTO
    labelTesto = Label(window, text="Testo Mail")
    # Qui viene usato Text invece che Entry perché permette di aumentare l'altezza della finestra
    testoEntry = Text(window, width=25, height=10, borderwidth=2, relief="groove")
    testoEntry.configure(font="Aria")  # Configuro manualmente il font
    testoInvio = ttk.Button(window, text="Invio", command=lambda: testoEmail(window, testoEntry))

    # DICHIARAZIONI INVIA MAIL
    inviaMail = ttk.Button(window, text="Invia Newsletter", command=lambda: verificaInvioNewsletter(window, oggettoMail, username, password))

    # POSIZIONI AGGIUNTA DI UNA MAIL
    labelInserimento.place(x=330, y=350)
    mailInserita.place(x=360, y=370)
    ricerca.place(x=415, y=400)
    labelPresente.place(x=410, y=425)

    # POSIZIONI ALLEGA FILE
    labelAllegato.place(x=0, y=130)
    allegato.place(x=60, y=153)
    labelFileScelto.place(x=380, y=143)

    # POSIZIONI ALLEGA OGGETTO
    labelOggetto.place(x=0, y=40)
    oggettoEntry.place(x=0, y=63)
    oggettoInvio.place(x=63, y=93)

    # POSIZIONI ALLEGA TESTO
    labelTesto.place(x=0, y=190)
    testoEntry.place(x=0, y=213)
    testoInvio.place(x=63, y=385)

    # POSIZIONI INVIA MAIL
    inviaMail.place(x=415, y=285)

    window.mainloop()


root.mainloop()


# TODO: eliminazione di una mail
"""
# DICHIARAZIONI ELIMINAZIONE DI UNA MAIL
# eliminazione = ttk.Button(window, text="Elimina mail", command=ricercaElim)

# POSIZIONI ELIMINAZIONE DI UNA MAIL
# eliminazione.place(x=110, y=50)

# FUNZIONE PER ELIMINARE UNA MAIL DALLA LISTA
def ricercaElim():

    riempiLista()  # devo richiamarlo per fare in modo che la lista sia sempre aggiornata
    for i in indirizzi:
        if name.get() == i:
            labelPresente.config(text="Email presente")
            elimina()
            return
        else:
            labelPresente.config(text="Email assente")


def elimina():

    # PORZIONE DI CODICE PER ELIMINARE UNA MAIL
    with open("testo.txt", "r") as ft:

        lines = ft.readlines()  # leggo tutto il file e lo metto in lines

    ft.close()

    with open("testo.txt", "w") as ft:

        for line1 in lines:  # se trovo name.get() scrivo una linea vuota cancellandolo

            if line1.strip("") != name.get():
                ft.write(line1)

    # TODO: PORZIONE DI CODICE PER PULIRE LE LINEE BIANCHE DAL FILE
"""

# ORIGINALE DELL'ELSE NELLA FUNZIONE testoEmail
"""
copiaTesto = Text(window, width=25, height=10)
copiaTesto.configure(font="Aria")  # Configuro manualmente il font
copiaTesto.insert(tk.END, inputTesto)
copiaTesto.place(x=380, y=213)
"""