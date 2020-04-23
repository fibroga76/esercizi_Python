import hashlib
import socket 
import flask

def getHash(string):
    m = hashlib.sha256()
    m.update(string)
    return m.hexdigest()

IP = "192.168.10.73"
PORT = 5000
method = "POST"
URL = "http://127.0.0.1:5000/register"
version = "HTTP/1.0"
username = "useruseruser"
password = getHash("123456")


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    #creazione oggetto socket per connessione al server 
s.connect((IP,PORT))

body_entity = f"username={username}&password={password}"    #formazione body entity del messaggio concatenando username e password

headers = f"Content-Type: application/x-www-form-urlencoded\nContent-Length: {len(body_entity)}" #formazione dell'header del messaggio con content type e content length 

request = f"{method} {URL} {version}\n{headers}\n\n{body_entity}"   #formazione completa messaggio con metodo e url


'''

Messaggio con Metodo GET che viene inviato al web server in flask
 
s.send(f"{method} {URL}  {version}\n\n".encode())       send del messaggio HTTP contenente la GET
 
data="none" 

out_file = open("file_get.html","w")    apertura file per salvataggio risposta dal web server
while data != "":
    data = s.recv(4096).decode()        ricezione e decodifica della risposta
    out_file.writelines(data)           scrittura su file della risposta 
    #print(data)
out_file.close()                        #chiusrsa file

s.close()
exit(0)'''

#messaggio con metodo POST per registrazione al web server
s.send(request.encode())
out_file = open("file_post.html","w")   #apertura file per salvataggio pagina di registrazione 
data="none"
while data != "":
    data = s.recv(4096).decode()    #fin quando non ci sono più righe, stampo il messaggio di risposta del server che contiene la pagina di registrazione 
    out_file.writelines(data)       #scrittura sul file
    #print(data)
out_file.close()    #chiususra del file

s.close()   #chiusura del socket