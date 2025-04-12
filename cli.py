import click
from core.campaign import launch

@click.group()
def cli():
  """A cli interface for the deep phish security app"""
  pass

cli.add_command(launch)

if __name__ == "__main__":
  cli()