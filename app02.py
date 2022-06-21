import mysql.connector
from flask import Flask, request, url_for, flash, redirect, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QWERTYUIOP1234567890'  
CORS(app)

def get_db_connection():
    conn = mysql.connector.connect(host="localhost",   user="root",   password="TeleJei2123medicina",   database="db_post" )
    return conn
    
def get_post(post_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM posts WHERE id = %s',(post_id,))
    post = cur.fetchone()
    conn.close()
    if post is None:
        return False
    return post
    

@app.route('/posts')
def jsonposts():
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM posts order by created desc')
    posts = cur.fetchall()
    conn.close()
    return jsonify(posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return jsonify(post)


@app.route('/<int:post_id>/comments')
def comments(post_id):
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    valori=(post_id,)
    cur.execute('SELECT * FROM comments where id_post = %s  order by id_post',valori)
    comments = cur.fetchall()
    conn.close()
    return jsonify(comments)


@app.route('/creaPost', methods=['GET'])
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


@app.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.json['title']
        content = request.json['content']
        cat = request.json['category']
        if not title:
            return json.dumps({'message': 'titolo richiesto'});    
        else:
            conn = get_db_connection()
            cur=conn.cursor(dictionary=True)
            cur.execute('UPDATE posts SET title = %s, content = %s'
                         ' WHERE id = %s',
                         (title, content, cat, id))
            conn.commit()
            conn.close()
            return json.dumps({'message': 'modifica avvenuta'});  
    return jsonify(post)
    # return render_template('edit.html', post=post)


@app.route('/delete', methods=['POST'])
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    cur=conn.cursor(dictionary=True)
    cur.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return json.dumps({'message': 'cancellato'})