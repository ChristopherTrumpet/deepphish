import click
from core.campaign import launch
from core.templates import create_template

@click.group()
def cli():
  """A cli interface for the deep phish security app"""
  pass

cli.add_command(launch)
cli.add_command(create_template)

if __name__ == "__main__":
  cli()