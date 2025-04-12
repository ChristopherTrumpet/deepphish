import sqlite3
from core.client import Client

con = sqlite3.connect(":memory:")

def insert_client(client):
  with con:
    c.execute("INSERT INTO client VALUES (:name, :industry, :contact_email, :config_path)", {'name': client.name, 'industry': client.industry, 'contact_email' : client.email, 'config_path' : client.config})
  con.commit()

def get_client_by_name(name):
  c.execute("SELECT * FROM client WHERE name=:name", {'name': name})
  return c.fetchall()

c = con.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS client (
            name text,
            industry text,
            contact_email text,
            config_path text
            )""")