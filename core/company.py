import click

@click.command()
@click.option('-n', '--name', type=str, required=True)
@click.option('-i', '--input-type', type=click.Choice(['csv']), required=True)
def add_client(name: str, input_type: str):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--campaign-id', type=int)
def fetch_results(client: str, cid: int):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
def classify(client: str) -> dict:
  pass

@click.command()
@click.option('-c', '--client', type=str)
def remove_client(client: str):
  pass

@click.command()
def list_clients():
  pass