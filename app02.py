import mysql.connector
from flask import Flask, request, url_for, flash, redirect, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QWERTYUIOP1234567890'  
CORS(app)

#collegamento db 
def get_db_connection():
    conn = mysql.connector.connect(host="localhost",   user="root",   password="TeleJei2123medicina",   database="db_post" )
    return conn

#funzione utilizzata per richiamare l'id del post da db.
def get_post(post_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM posts WHERE id = %s',(post_id,))
    post = cur.fetchone()
    conn.close()
    if post is None:  # se il id del post non funziona ritorna False. 
        return False
    return post
    
#funzione utilizzata per richiamare quando il post è stato creato da db, in ordine decrescente.
@app.route('/posts')
def jsonposts():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM posts order by created desc')
    posts = cur.fetchall()
    conn.close()
    return jsonify(posts)

#
@app.route('/posts/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return jsonify(post)


@app.route('/comments/<int:post_id>')
def comments(post_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    valori=(post_id,)
    cur.execute('SELECT * FROM comments where id_post = %s  order by id_post',valori)
    comments = cur.fetchall()
    conn.close()
    return jsonify(comments)


@app.route('/creapost', methods=['GET'])
def creaPost():
    title = request.json['title'] 
    content = request.json['content']
    cat = request.json['category']
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('INSERT INTO posts (title, content,category) VALUES (%s, %s,%s)',
                    (title, content, cat))
    conn.commit()
    lastid = cur.lastrowid
    objson = { "message": "post creato correttamente", "id":lastid}
    objson= jsonify(objson)
    conn.close()
    return objson

#funzione per edit post
@app.route('/editpost/<int:id>', methods=['PATCH'])
def edit(id):
    post = get_post(id)
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('UPDATE`db_post`.`posts` SET title = %s, content = %s'' WHERE id = %s')
    conn.commit()
    conn.close()
    return jsonify(post)

#funzione utillizata per cancellare un post dal db
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('DELETE FROM posts WHERE id = %s', (id))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return json.dumps({'message': 'cancellato'})