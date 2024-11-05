"""
This is the main application file for the Flask app.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from flask_session import Session
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)
Session(app)


if __name__ == '__main__':
    app.run(debug = True)


@app.route("/")
def homepage():
    """
    Redirects the user to the login page.
    """
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles the signup form. If the request is a GET, renders the login.html
    template with is_login set to False. If the request is a POST, attempts to
    create a new user in the database. If successful, flashes a success message
    and redirects the user to the login page. If the username already exists,
    flashes a warning message and renders the login.html template with is_login
    set to False.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            mysql.connection.commit()
            flash('Account created! Please log in.', 'success')
            return render_template('login.html', is_login=True)
        except Exception as e:
            flash('Username already exists. Please try again.', 'warning')
            return render_template('login.html', is_login=False)
        finally:
            cur.close()
    return render_template('login.html', is_login=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the login form. If the request is a GET, renders the login.html
    template with is_login set to True. If the request is a POST, attempts to
    log the user in. If successful, sets the session['username'] variable to the
    username and redirects the user to the main page. If the username or
    password is invalid, flashes a warning message and renders the login.html
    template with is_login set to True.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('main'))
        else:
            flash('Invalid Username or Password. Please try again.', 'warning')
    return render_template('login.html', is_login=True)


@app.route('/logout')
def logout():
    """
    Logs the user out by removing the session['username'] variable and
    redirecting the user to the login page.
    """
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/main')
def main():
    """
    Renders the index.html template if the user is logged in. If the user is not
    logged in, redirects the user to the login page.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])


@app.route('/sort', methods=['GET'])
def sort():
    """
    Handles the sorting of the countries. Gets the search query, criteria, and
    sort order from the request arguments. Queries the database and returns the
    results as a JSON object.
    """
    search_query = request.args.get('search', '')
    criteria = request.args.get('criteria', 'Name')
    sort_order = request.args.get('sort_order', 'asc')

    cur = mysql.connection.cursor()
    query = f"SELECT Name, Population FROM country WHERE Name LIKE %s ORDER BY {criteria} {sort_order.upper()}"
    search_term = f"%{search_query}%"
    cur.execute(query, (search_term,))
    results = cur.fetchall()
    cur.close()
    return jsonify(results)

