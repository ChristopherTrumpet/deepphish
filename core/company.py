import click
from core.utils import import_csv
from core.client import Client
from data.db import insert_client, get_client_by_name

@click.command()
@click.option('-n', '--name', type=str, required=True)
@click.option('-i', '--input-type', type=click.Choice(['csv']), required=True)
@click.option('-f', '--file', type=str)
def add_client(name: str, input_type: str, file: str):
  csv_data = import_csv(file)
  for row in csv_data:
    c = Client(row[0], row[1], row[2], row[3])
    insert_client(c)
  click.echo(get_client_by_name(name))
@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--campaign-id', type=int)
def fetch_results(client: str, cid: int):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
def classify(client: str) -> dict:
  pass

@click.command()
@click.option('-c', '--client', type=str)
def remove_client(client: str):
  pass

@click.command()
def list_clients():
  pass