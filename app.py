from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'LQ</>2006mimi:M'
app.config['MYSQL_DB'] = 'todo_app'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM todos')
    todos = cursor.fetchall()
    cursor.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    description = request.form.get('description')
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO todos (title, description) VALUES (%s, %s)', (title, description))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_todo(id):
    title = request.form.get('title')
    description = request.form.get('description')
    completed = request.form.get('completed') == 'on'
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE todos SET title=%s, description=%s, completed=%s WHERE id=%s', (title, description, completed, id))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM todos WHERE id=%s', (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
