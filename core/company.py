import click
from core.utils import import_csv, split_department
from core.client import Client
from core.employee import Employee
from data.db import insert_client, get_client_by_name, get_employees, insert_employee, print_me

from risk_model.deployment import predict

@click.command()
@click.option('-n', '--name', type=str, required=True)
@click.option('-id', '--industry', type=str, required=True)
@click.option('-e', '--email', type=str,  required=True)
@click.option('-c', '--config', type=str, required=True)
@click.option('-it', '--input-type', type=click.Choice(['csv']), required=True)
@click.option('-f', '--file', type=str)
def add_client(name: str, industry: str, email: str, config: str, input_type: str, file: str):
  c = Client(name, industry, email, config)
  csv_data = import_csv(file)
  
  insert_client(c)

  for row in csv_data:
    e = Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    insert_employee(e)

  print_me()

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
    click.echo(data[0])
    output = []
    for row in data:
      # Name, Lit Score, Seniority, Degree Type, Gender, Department_HR, Department_Engineering, Age
      # TODO Check this out to see if it works
      t = split_department(row[8])

      department_HR = t[0]
      department_IT = t[1]

      output.append(predict(row[3], row[4], row[5], row[6], row[7], department_HR, department_IT, row[9])) 

    return output
  return None

@click.command()
@click.option('-c', '--client', type=str)
def remove_client(client: str):
  pass

@click.command()
def list_clients():
  pass