import mysql.connector
from flask import Flask, jsonify, redirect, json, url_for, request
from flask_cors import CORS

#creo connessione con MYSQL
def get_db_connection():             #funzione per connettere MYSQL 
    conn = mysql.connector.connect(host="localhost",   user="root",   password="TeleJei2123medicina",   database="db_post" )
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QWERTYUIOP1234567890'   #parte fissa
CORS(app)

def get_post(post_id):    # funzione che allega l'id del post da MYSQL
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM posts WHERE id = %s',(post_id,))
    post = cur.fetchone()
    conn.close()
    if post is None:
        return False
    return post

@app.route('/')
def jsonposts():                       # funzione post jason
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM posts order by created desc")
    posts = cur.fetchall()
    conn.close()
    return jsonify(posts)

@app.route('/creaPost', methods=['POST'])
def creaPost():
    title = request.json['title'] #recupero il title da oggetto json
    content = request.json['content']
    cat = request.json['category']
    #creo connessione
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('INSERT INTO posts (title, content,category) VALUES (%s, %s,%s)', (title, content,cat))
    conn.commit()
    #eseguo query insert
    #recupero id ultimo record inserito da cursore
    lastid = cur.lastrowid; 
    #creo oggetto dictonary python
    objson = { "message": "post creato correttamente", "id": lastid}
    #chiudo la connessione
    conn.close()
    #la mia chiamata ritorna una stringa di testo in formato json
    return jsonify(objson)

@app.route('/edit', methods=('GET', 'POST'))
def edit(id):                                  # funzione che permette di editare i post
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            return json.dumps({'message': 'creazione post not found'});
        else:
            conn = get_db_connection()
            cur=conn.cursor(dictionary=True)
            cur.execute('UPDATE posts SET title = %s, content = %s'
                         ' WHERE id = %s',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    

@app.route('/<int:post_id>')   
def post(post_id):
    post = get_post(post_id)
    if(post==False):
        return json.dumps({'message': 'id not found'})
    return jsonify(post)

@app.route('/<int:post_id>/comments')
def comments(post_id):                # funzione che richiama i commenti dei post trasformandoli prima in stringhe json
    conn = get_db_connection() 
    cur=conn.cursor(dictionary=True)
    valori = (post_id,)
    cur.execute("SELECT * FROM comments where idpost = %s order by idpost", valori)
    comments = cur.fetchall()
    conn.close()
    return jsonify(comments)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(post_id):                                     # funzione che permette di cancellare il post 
    post = get_post(post_id)
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    if (post== delete):
        return  json.dumps({'message': 'was successfully deleted!' + ['id']})
    #flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))