import click
from data.db import DatabaseManager
from api.requests import start_dash_server

@click.command()
@click.option('-c', '--client', help='Client for launching campaign', required=True, type=str)
def launch(client, template):
  """Start a phishing campaign for a specific client
  Retrieve specified template from database, and start an automated attack on the specified client.
  This attack needs to retrive and sent emails to a ratio of risk and risk averse employees using the risk classification system

  Args:
    client: Company to target campaign towards
    template: Email template stored in ./templates

  """
  click.echo(f"launching campaign for {client}")

@click.command()
@click.option('-cid', '--campaign-id', help="Stops the specified campaign", required=True, type=int)
def stop_campaign():
  pass


@click.command()
@click.option('--company-name')
@click.option('--type')
@click.option('--start-time')
@click.option('--end-time')
@click.option('--status')
@click.option('--description')
def create_campaign(company_name, type, start_time, end_time, status, description): 
  db_manager = DatabaseManager()

  company_id = db_manager.get_company_by_name(company_name=company_name)

  db_manager.create_campaign(company_id, type, start_time, end_time, status, description)

  click.echo(get_campaigns(company_id))

def get_campaigns(company_id): 
  db_manager = DatabaseManager()

  return db_manager.get_campaigns(company_id)

@click.command()
def dashboard():
  dashboard_path = "../dashboard/"
  nextjs_process = start_dash_server(dashboard_path)