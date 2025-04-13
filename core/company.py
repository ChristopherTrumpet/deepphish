import click
import uuid
from risk_model.deployment import predict
from data.db import DatabaseManager
from core.utils import import_csv

@click.command()
@click.option('-n', '--name', type=str, required=True)
@click.option('-e', '--email', type=str, required=True)
@click.option('-i', '--input-type', type=click.Choice(['csv']), required=True)
@click.option('-f', '--file', type=str)
def add_client(name: str, email: str, input_type: str, file: str):

  csv_data = []
  if (input_type == "csv"):
    csv_data = import_csv(file)

  db_manager = DatabaseManager()
  company_id = db_manager.create_company(name, email)
  for row in csv_data:
    employee_id = db_manager.add_employee_to_company(company_id, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    if (employee_id):
      click.echo(f"Employee added with ID: {employee_id}")
      employee = db_manager.get_employee(employee_id)
      if employee:
          print(f"Retrieved employee: {employee}")
  db_manager.close()
  return company_id


@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--campaign-id', type=int)
def fetch_results(client: str, cid: int):
  pass

@click.command()
@click.option('-c', '--client-name', type=str, required=True)
def classify(client_name: str) -> dict:
  db_manager = DatabaseManager()
  client_id = str(uuid.uuid4())
  company = db_manager.get_company(client_id)
  if company:
    click.echo("Retrived company: {company}")

@click.command()
@click.option('-c', '--client', type=str)
def remove_client(client: str):
  pass

@click.command()
def list_clients():
  pass