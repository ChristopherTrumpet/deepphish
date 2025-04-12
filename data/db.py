import sqlite3
from core.client import Client

con = sqlite3.connect(":memory:")

def insert_client(client):
  with con:
    c.execute("INSERT INTO client (name, client_id, industry, contact_email, config_path) VALUES (:name,:client_id, :industry, :contact_email, :config_path)", {'name': client.name, 'client_id': client.client_id, 
                                                                                                        'industry': client.industry, 'contact_email' : client.email, 
                                                                                                        'config_path' : client.config})
  con.commit()

def insert_employee(emp):
  # {name: []}
  with con:
    c.execute('INSERT INTO employee (client_id, employee_id, name, email, literacy_score, seniority, degree_type, gender, department, age, risk_text, risk_value) VALUES (:client_id, :employee_id, :name, :email, :literacy_score, :seniority, :degree_type, :gender, :department, :age, :risk_text, :risk_value)', 
              {'client_id': emp.client_id, 'employee_id': emp.employee_id, 'name': emp.employee_name, 'email': emp.email, 'literacy_score': emp.literacy_score, 'seniority': emp.seniority, 
               'degree_type': emp.degree_type, 'gender': emp.gender, 'department': emp.department, 'age': emp.age, "risk_text": "Null", "risk_value": -1})
  con.commit()

def get_client_by_name(name):
  c.execute("SELECT * FROM client WHERE name=:name", {'name': name})
  return c.fetchall()

def get_employees(client):
  c.execute("SELECT * FROM employee WHERE client_name=:client", {'client': client.name})

def get_templates():
  c.execute("")

c = con.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS client (
            client_id text PRIMARY KEY, 
            name text, 
            industry text,
            contact_email text,
            config_path text
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS employee (
              employee_id TEXT PRIMARY KEY,
              client_id TEXT,
              name TEXT,
              email TEXT,
              literacy_score INTEGER,
              seniority INTEGER,
              degree_type INTEGER,
              gender INTEGER,
              department TEXT,
              age TEXT,
              risk_text TEXT,
              risk_value REAL, 
              FOREIGN KEY(client_id) REFERENCES client(client_id)
          )""")

