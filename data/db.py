import sqlite3
from core.client import Client

con = sqlite3.connect(":memory:")

def insert_client(client):
  with con:
    c.execute("INSERT INTO client VALUES (:name, :industry, :contact_email, :config_path)", {'name': client.name, 'industry': client.industry, 'contact_email' : client.email, 'config_path' : client.config})
  con.commit()

def insert_employee(emp):
  # {name: []}
  with con:
    c.executemany('INSERT INTO employee (name, email, literacy_score, seniority, degree_type, gender, department, age)', emp)

def get_client_by_name(name):
  c.execute("SELECT * FROM client WHERE name=:name", {'name': name})
  return c.fetchall()

def get_employees(client):
  c.execute("SELECT * FROM employee WHERE client_name=:client", {'client': client.name})

def get_templates():
  c.execute("")

c = con.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS client (
            name text PRIMARY KEY,
            industry text,
            contact_email text,
            config_path text
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS employee (
            FOREIGN KEY (client_name) REFERENCES client(name), 
            email text, 
            literacy_score int, 
            seniority int, 
            degree_type int, 
            gender int, 
            department text,
            age text,
            risk_text text, 
            risk_value float, 
          )""")

c.execute("""CREATE TABLE IF NOT EXISTS template (
            
          )""")