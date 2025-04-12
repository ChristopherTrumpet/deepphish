import click

@click.command()
@click.option('--client', help='Client for launching campaign', required=True)
def launch():
  """Start a phishing campaign for a specific client"""
  click.echo("launching campaign")

if __name__ == "__main__":
  launch()