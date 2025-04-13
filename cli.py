import click
from core.campaign import launch, dashboard
from core.templates import create_template, list_templates, delete_template, view_template
from core.company import add_client, classify, remove_client, list_clients
from core.campaign import create_campaign
from core.reporting import generate_debrief, generate_report, send_debrief, simulate_call, get_report, send_report

@click.group()
def cli():
  """A cli interface for the deep phish security app"""
  pass

# Campaigning
cli.add_command(launch)
cli.add_command(dashboard)

# Reporting
cli.add_command(generate_debrief)
cli.add_command(generate_report)
cli.add_command(send_debrief)
cli.add_command(simulate_call)
cli.add_command(generate_report)
cli.add_command(get_report)
cli.add_command(send_report)

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

# Campaign commands
cli.add_command(create_campaign)



if __name__ == "__main__":
  cli()