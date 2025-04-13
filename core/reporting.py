import click
from reports.md_builder import get_phishing_data
from data.db import DatabaseManager

@click.command()
@click.option('-c', '--company-name', type=str, required=True)
def generate_report(company_name: str):
  db_manager = DatabaseManager()
  company_id = db_manager.get_company_by_name(company_name)
  get_phishing_data(company_id)
  db_manager.close()

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--campaign', type=str, required=True)
def generate_debrief(client: str, cid: int):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--client', type=int, required=True)
def send_debrief(dest: str):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--client', type=int, required=True)
@click.option('-f', '--format', type=str, required=True)
def get_report(client: str, cid: int, format: str):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--client', type=int, required=True)
@click.option('-t', '--to', type=str, required=True)
def send_report(client: str, cid: int, to: str):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--client', type=int, required=True)
@click.option('-t', '--to', type=str, required=True)
def simulate_call(client: str, cid: int, to: str):
  pass