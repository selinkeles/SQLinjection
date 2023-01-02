from flask import Flask, jsonify, redirect, request, Response
import requests
import sqlite3
import random
import string
import time
import logging
from flask import render_template, url_for, redirect

# CREATE APP
app = Flask(__name__)
# SPECIFY DATABASE PATH
filepath = "instance\database.db"
# DATABASE CONNECTION
connection = sqlite3.connect(filepath)
cursor = connection.cursor()

# FOR CREATING RANDOM 1000 POSTS
# EXECUTED ONLY ONCE
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


# HOME ROUTE
@app.route("/")
def home():
    title = "Welcome"

    return render_template('home.html', title=title)


# SET UP LOGGING
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
# END LOGGING


# BLACKLIST ITEMS FOR POSTS
blaclistedPost = ["--", ";--", ";", "/*", "*/", "@@", "@", "char", "nchar", "varchar", "nvarchar", "alter", "begin", "cast", "create", "cursor", "declare", "delete",
                  "drop", "end", "exec", "execute", "fetch", "insert",
                  "kill", "open", "select", "sys", "sysobjects", "syscolumns",
                                                "table", "update", "%", " ", "or", "and", "+", "*", "\"", "\'", "=", "?"]

# BLACKLIST ITEMS FOR LOGIN
blaclistedLogin = ["--", ";--", ";", "/*",
                   "*/", "@@", " ", "+", "\"", "\'", "=", "?"]


# POST API
@app.route("/api/posts", methods=['GET'])
def result():
    pure = True
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    post_id = request.args.get("post_id")
    if post_id is None:
        query = "SELECT * FROM posts"
        results = cursor.execute(query)
        results = results.fetchall()
        return render_template('posts.html', posts=results)
        # return jsonify(results)
    post_id.lower()
    # Use of blacklist protection starts here
    for item in blaclistedPost:
        if item in post_id:
            pure = False
            break
    if pure:
        query = "SELECT * FROM posts WHERE post_id=%s" % post_id
        search_query = cursor.execute(query)
        post = search_query.fetchall()
        connection.close()
        # return jsonify(post)
        return render_template('posts.html', posts=post)
    else:
        errorMsg = "ERROR!!"
        return errorMsg


# LOGIN API
@app.route('/login', methods=['GET', 'POST'])
def login():
    pure = True
    title = "Login"
    # When method is post, submit request
    if request.method == 'POST':
        connection = sqlite3.connect(filepath)
        cursor = connection.cursor()
        email = request.form["email"]
        if email != None:
            email.lower()
        password = request.form["password"]
        if password != None:
            password.lower()
        # Use of blacklist protection starts here
        for item in blaclistedLogin:
            if item in email:
                pure = False
            elif item in password:
                pure = False
        if pure:
            cursor.execute(
                "SELECT * FROM users WHERE email = '%s'AND password = '%s'" % (email, password))
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
            return "ERROR!!"
    # When method is get, render login page
    else:
        return render_template('login.html', title=title)


@app.route('/<usr>')
def user(usr):
    title = "User"
    return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
