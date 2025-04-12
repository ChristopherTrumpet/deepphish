import click
from core.campaign import launch
from core.templates import create_template, list_templates, delete_template, view_template
from core.company import add_client, classify, remove_client, list_clients

@click.group()
def cli():
  """A cli interface for the deep phish security app"""
  pass

# Campaigning
cli.add_command(launch)

# Templates
cli.add_command(create_template)
cli.add_command(delete_template)
cli.add_command(view_template)
cli.add_command(list_templates)

# Company commands
cli.add_command(add_client)
cli.add_command(remove_client)
cli.add_command(classify)
cli.add_command(list_clients)


if __name__ == "__main__":
  cli()