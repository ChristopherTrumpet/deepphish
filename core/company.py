import click
from core.utils import import_csv, split_department
from core.client import Client
from core.employee import Employee
from data.db import insert_client, get_client_by_name, get_employees

from risk_model.deployment import predict

@click.command()
@click.option('-n', '--name', type=str, required=True)
@click.option('-i', '--input-type', type=click.Choice(['csv']), required=True)
@click.option('-f', '--file', type=str)
def add_client(name: str, input_type: str, file: str):
  csv_data = import_csv(file)
  for row in csv_data:
    e = Employee(row[0], row[1], row[2], row[3])
    insert_client(e)

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--campaign-id', type=int)
def fetch_results(client: str, cid: int):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
def classify(client: str) -> dict:
  if client != None: 
    data = get_employees(client)
    output = []
    for row in data:
      # Name, Lit Score, Seniority, Degree Type, Gender, Department_HR, Department_Engineering, Age
      # TODO Check this out to see if it works
      t = split_department(row[5])

      department_HR = t[0]
      department_IT = t[1]

      output.append(predict(row[0], row[1], row[2], row[3], row[4], department_HR, department_IT, row[6])) 

@click.command()
@click.option('-c', '--client', type=str)
def remove_client(client: str):
  pass

@click.command()
def list_clients():
  pass