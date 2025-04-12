import sqlite3
from core.client import Client

con = sqlite3.connect(":memory:")

def insert_client(client):
  with con:
    c.execute("INSERT INTO client VALUES (:name, :industry, :contact_email, :config_path)", {'name': client.name, 'industry': client.industry, 'contact_email' : client.email, 'config_path' : client.config})
  con.commit()

def insert_employee(emp):
  with con:
    c.executemany('INSERT INTO employee (name, department, age, seniority)')

def get_client_by_name(name):
  c.execute("SELECT * FROM client WHERE name=:name", {'name': name})
  return c.fetchall()

def get_employees(client):
  pass

def get_templates():
  c.execute("")

c = con.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS client (
            name text,
            industry text,
            contact_email text,
            config_path text
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS employee (
            name text,
            department text,
            age text,
            seniority text
          )""")

c.execute("""CREATE TABLE IF NOT EXISTS template (
            
          )""")