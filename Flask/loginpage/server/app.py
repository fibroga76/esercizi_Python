import hashlib
from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

def getHash(string):
    m = hashlib.sha256()
    m.update(string)
    return m.hexdigest()

def validate(username, password):
    completion = False
    with sqlite3.connect('static/db.db') as con:    #mantiene in memoria quest'oggetto solo durante il tempostrettamente necessario a compiere tutte le operazioni sull'oggetto
        cur = con.cursor()
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[0]
            dbPass = row[1]
            if dbUser == username:
                completion = check_password(dbPass, password)
    return completion

def insertDB(username, password):
    with sqlite3.connect('./static/db.db') as con:
        cur = con.cursor()
        try:
            cur.execute(f'INSERT INTO USERS (USERNAME, PASSWORD) VALUES ("{username}", "{password}")')      #inserisce password nel database
        except Exception:
            pass
        

def check_password(hashed_password, user_password):         #controlla hash della password inserita ed hash della password sul database
    return hashed_password == getHash(user_password)


@app.route('/', methods=['GET', 'POST'])
def signInOrSignUp():                                       #pagina iniziale che in base al pulsante che premiamo sull'HTML redireziona sulla pagina di login oppure di registrazione
    error = None
    if request.method == 'POST':
        if request.form['submit_button'] == 'Log-In':
            return redirect(url_for('login'))
        elif request.form['submit_button'] == 'Sign-Up':
            return redirect(url_for('register'))
        else:
            pass # unknown
        
    return render_template('index.html', error = error)


@app.route('/login', methods=['GET', 'POST'])    #lo '/' indica che si trova nella prima pagina
def login():
    error = None
    if request.method == 'POST':                #se il metodo che riceve dal messaggio HTTP è post, prende username e password, altrimenti restituisce nuovamente il template del login page
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)       #funzione che verifica le credenziali nel database
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('secret'))

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':                            #funzione register che salva le nuove credenziali nel database
        username = request.form['username']
        password = request.form['password']
        insertDB(username, password)

    return render_template('register.html', error=error)

@app.route('/secret')       #redirect ad una nuova pagina con indirizzo /secret
def secret():
    return "This is a secret page!"

if __name__== "__main__":   #chiamata al main "riciclabile" 
    app.run()