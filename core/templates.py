import click

from data.db import get_templates

@click.command()
@click.option('-n', '--name', type=str, required=True, help="Name of the template for identification")
@click.option('-d', '--difficulty', type=click.Choice(['easy', 'medium', 'hard'], case_sensitive=False), required=True, help="Difficulty of template")
def create_template(name: str, difficulty: str):
  pass

@click.command()
@click.option('-n', '--name', type=str, required=True)
def view_template(name: str):
  pass

@click.command()
@click.option('-cid', '--company-id', type=int, required=False)
def list_templates(c_id):
  get_templates()
  pass

@click.command()
@click.option('-n', '--name', type=str, required=True)
def delete_template(name):
  pass