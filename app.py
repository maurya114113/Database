from flask import Flask, render_template, request, redirect, session
import mysql.connector
from config import db_config

app = Flask(__name__)
app.secret_key = 'secretkey'

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user['username']
            session['role'] = user['role']

            if user['role'] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/user')
        else:
            return "Invalid credentials"

    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    if 'username' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html', username=session['username'])
    return redirect('/')

@app.route('/user')
def user_dashboard():
    if 'username' in session and session['role'] == 'user':
        return render_template('user_dashboard.html', username=session['username'])
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
