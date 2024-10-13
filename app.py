import sqlite3
from flask import Flask, render_template, request, g, redirect

app = Flask(__name__)

DATABASE_FILE = 'employees.db'

# Get a useable connection to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_FILE)
        db.row_factory = sqlite3.Row
    return db

# Close the database connection when the app shuts down
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# return the results from a database query
def db_query(query, args=()):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return rv

# execute a database query
def db_execute(query, args=()):
    conn = get_db()
    conn.execute(query, args)
    conn.commit()
    conn.close()
    return True

def create_employee(name, email, salary):
    db_execute("INSERT INTO employees (name, email, salary) VALUES (?, ?, ?);", (name, email, salary))
    

def get_employees_from_db():
    return db_query("SELECT * FROM employees")

def get_employee_from_db(employee_id):
    results = db_query("SELECT * FROM employees WHERE id = ?;", [employee_id])
    if results:
        return results[0]
    else:
        return None

@app.get('/')
def index():
    employees = get_employees_from_db()
    return render_template('employees.html', employees=employees)

@app.get('/employees/<employee_id>')
def show_employee(employee_id):
    employee = get_employee_from_db(int(employee_id))
    return render_template("employee.html", employee=employee)

@app.get('/new_employee')
def new_employee():
    return render_template("new_employee.html")

@app.post('/new_employee')
def add_employee():
    name = request.form.get('name')
    email = request.form.get('email')
    salary = request.form.get('salary')
    create_employee(name, email, salary)
    return redirect('/')
