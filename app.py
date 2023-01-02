# .\venv\Scripts\activate
# python -m flask --app .\app.py run
from flask import Flask, jsonify, redirect, request, Response
import requests
import sqlite3
import random
import string
import time
import logging
from flask import render_template, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# #app.config['SECRET_KEY'] = 'thisisasecretkey'
# db = SQLAlchemy(app)
filepath = "instance\database.db"


# class User(db.Model,UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(80), nullable=False)
#     password = db.Column(db.String(80), nullable=False)


# class Posts(db.Model):
#     post_id = db.Column(db.Integer, primary_key=True)
#     post_content = db.Column(db.String(80), nullable=False)

#     def __init__(self,post_content):
#         self.post_content = post_content


posts = []
connection = sqlite3.connect(filepath)
cursor = connection.cursor()
# for i in range(1000):
#     random_content = ''.join(random.choices(
#         string.ascii_letters + string.digits, k=8))
#     posts.append(
#         {'post_id': i, 'post_content': random_content}
#     )
#     query = "INSERT OR REPLACE INTO posts VALUES({id},'{text}')".format(
#         id=i, text=random_content)
#     cursor.execute(query)
#     connection.commit()

users = [
    {
        'email': 'selin@selin.com', 'password': '1234'
    }
]


@app.route("/")
def home():
    title = "Welcome"

    return render_template('home.html', title=title)



# set up logging
logging.basicConfig(filename='request_logs.txt', level=logging.INFO)

@app.before_request
def log_request_data():
    """Logs the request data."""
    logging.info('{} {}'.format(request.method, request.url))

@app.after_request
def log_response_data(response):
    """Logs the response data."""
    logging.info('Response status: {}'.format(response.status_code))
    logging.info('Response data: {}'.format(response.data))
    return response


@app.route("/api/posts", methods=['GET'])
def result():
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    post_id = request.args.get("post_id")
    if post_id is None:
        query = "SELECT * FROM posts"
        post = cursor.execute(query)
        post = post.fetchall()
        return jsonify(post)
    # remove try-except block and finally block
    query = "SELECT * FROM posts WHERE post_id=%s" % post_id
    search_query = cursor.execute(query)
    post = search_query.fetchall()
    connection.close()
    return jsonify(post)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    if request.method == 'POST':
        connection = sqlite3.connect(filepath)
        cursor = connection.cursor()
        email = request.form["email"]
        password = request.form["password"]
        cursor.execute("SELECT * FROM users WHERE email = '%s'AND password = '%s'" % (email, password))
        user = cursor.fetchone()
        if user:
            user = {'email': email, 'password': password}
            connection.commit()
            connection.close()
            return redirect(url_for('user', usr=user))
        else:
            # credentials not found in database
            connection.commit()
            connection.close()
            return render_template('login.html', title=title, error='Invalid email or password')
    else:
        return render_template('login.html', title=title)


@app.route('/<usr>')
def user(usr):
    title = "User"
    return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
