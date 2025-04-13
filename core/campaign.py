import click
from core import query_email
from data.db import DatabaseManager
from api.requests import start_dash_server
from data.db import *

@click.command()
@click.option('-c', '--campaign-name', help="Stops the specified campaign", required=True, type=int)
@click.option('-cn', '--company-name', help="Stops the specified company", required=True, type=int)
def stop_campaign(company_name: str, campaign_name: str):
  db_manager = DatabaseManager()

  company_id = db_manager.get_company_by_name(company_name)
  campaign_id = db_manager.get_campaign(company_id, campaign_name)
  db_manager.update_campaign(company_id, campaign_name, status="completed")

@click.command()
@click.option('--company-name')
@click.option('--campaign-name')
@click.option('--type')
@click.option('--start-time')
@click.option('--end-time')
@click.option('--status')
@click.option('--description')
def create_campaign(company_name, campaign_name, type, start_time, end_time, status, description):
  db_manager = DatabaseManager()

  company_id = db_manager.get_company_by_name(company_name)
  campaign_id = db_manager.create_campaign(company_id, type, start_time, end_time, status, description)

  return campaign_id

@click.command()
@click.option('--company-name')
@click.option('--campaign-name')
def start_campaign(company_name, campaign_name):
  db_manager = DatabaseManager()

  company_id = db_manager.get_company_by_name(company_name)
  employees = db_manager.get_employees_by_company(company_id)
  campaign = db_manager.update_campaign(company_id, campaign_name, status="running")
  query_email.start_campaign(campaign, employees)


@click.command()
def dashboard():
  nextjs_process = start_dash_server()