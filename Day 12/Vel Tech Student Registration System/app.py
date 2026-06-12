from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# Create database and table
def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT NOT NULL,
            department TEXT NOT NULL,
            year INTEGER NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            gender TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# Initialize database
init_db()


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        roll_number = request.form['roll_number']
        department = request.form['department']
        year = request.form['year']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']
        address = request.form['address']

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO students
            (name, roll_number, department, year, email, phone, gender, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (name, roll_number, department, year, email, phone, gender, address)
        )

        conn.commit()
        conn.close()

        message = "Student Registered Successfully!"

        return render_template('register.html', message=message)

    return render_template('register.html')


# Students Page
@app.route('/students')
def students():

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    conn.close()

    return render_template('students.html', students=records)


# About Page
@app.route('/about')
def about():
    return render_template('about.html')


# Run Application
if __name__ == '__main__':
    app.run(debug=True)