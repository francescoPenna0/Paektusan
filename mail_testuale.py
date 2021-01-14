import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  # per includere oggetto e allegato bisogna usare il modulo MIMEMultipart
from email.mime.base import MIMEBase  # MIMEBase serve per codificare il file da usare come allegato
from email import encoders  # encoders trasforma l'allegato in base64

# PORZIONE DI CODICE PER LA CREAZIONE DELLA LISTA A CUI INVIARE LE MAIL
indirizzi = []
try:

    f = open("Risorse/testo/testo.txt", "r")
    line = f.readline().strip()

    while line != '':

        mail = line
        line = f.readline().strip()
        indirizzi.append(mail)

except IOError:
    print("Errore nel file da input\n")
except ():
    print("Unexpected error:", sys.exc_info()[0])
    raise

# CREDENZIALI USER E OGGETTO
email_user = <mail_user>
oggetto = 'PAEKTUSAN #3'

# MIMEPART PER GESTIRE SENDER RECEIVER E OGGETTO, RAPPRESENZA LA MAIL
msg = MIMEMultipart()  # ho creato un nuovo oggetto di Multipart e definisco le variabili
msg['From'] = email_user
# msg['To'] = email_user
msg['Subject'] = oggetto

# ATTACCO IL CONTENUTO DEL MESSAGGIO A MIMEPART QUINDI ALLA MAIL
contenuto = 'Il terzo episodio (ufficiale) di PAEKTUSAN che da oggi diventa trisettimanale, per adeguarsi alla ' \
            'nuova Fase ' \
            '2 nella quale non avrete più giornate infinite disperatamente bisognose di pretesti per ammazzare ' \
            'il tempo.'
msg.attach(MIMEText(contenuto, 'plain'))  # MIMEText è un oggetto che si attacca al quello di Multipart e contiene
# il corpo dell'email, plain perché è una semplice mail senza html ecc

# GESTIONE DELL'ALLEGATO
filename = 'PAEKTUSAN_3.pdf'
allegato = open(filename, 'rb')  # apro il file in modalità lettura binaria

p = MIMEBase('application', 'octet-stream')  # farò l'uploading del file attraverso MIMEBase quindi in Base64
p.set_payload(allegato.read())  # leggo il contenuto dell'allegato
encoders.encode_base64(p)  # base64 è l'encoding standard per le email (documentati quando hai tempo)
p.add_header('Content-Disposition', "attachment; filename = " + filename)  # aggiungo la descrizione del file

msg.attach(p)  # attacco il file pdf alla mail

testo = msg.as_string()  # come ultima cosa devo trasformare MIMEM in una stringa di testo perché sia inviabile

# MANDO LA MAIL CONNETTENDOMI AI SERVER GMAIL
mail = smtplib.SMTP('smtp.gmail.com', 587)  # uso i server gmail di smtp e specifico il numero della porta che uso

mail.ehlo()  # mi identifico ai server di google con helo o ehlo il primo per regolare, il secondo per l'extended smtp

# comincio la modalità tls, transport layer security, perché ora farò il login e devo criptare le credenziali
mail.starttls()

mail.login(email_user, '')  # login

for i in indirizzi:

    mail.sendmail(email_user, i, testo)  # .sendmail(sender, receiver, mail)

mail.close()  # chiudo il contatto col server
