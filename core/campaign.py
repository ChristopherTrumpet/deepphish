import click

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



if __name__ == "__main__":
  launch()