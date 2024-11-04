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
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
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
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/main')
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/sort', methods=['GET'])
def sort():
    search_query = request.args.get('search', '')
    criteria = request.args.get('criteria', 'Name')
    sort_order = request.args.get('sort_order', 'asc')

    if criteria not in ['Name', 'Population']:
        criteria = 'Name'

    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'

    cur = mysql.connection.cursor()
    query = f"SELECT Name, Population FROM country WHERE Name LIKE %s ORDER BY {criteria} {sort_order.upper()}"

    search_term = f"%{search_query}%"
    cur.execute(query, (search_term,))

    results = cur.fetchall()
    cur.close()
    return jsonify(results)
