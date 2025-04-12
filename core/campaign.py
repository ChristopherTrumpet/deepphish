import click

@click.command()
@click.option('-c', '--client', help='Client for launching campaign', required=True, type=str)
def launch(client):
  """Start a phishing campaign for a specific client"""
  click.echo(f"launching campaign for {client}")

@click.command()
@click.option('-cid', '--campaign-id', help="Stops the specified campaign", required=True, type=int)
def stop_campaign():
  pass



if __name__ == "__main__":
  launch()