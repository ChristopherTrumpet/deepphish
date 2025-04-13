import click
from core.utils import convert_markdown_to_pdf

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--campaign', type=int, required=True)
def generate_report(client: str, cid: int):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--campaign', type=str, required=True)
def generate_debrief(client: str, cid: int):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--client', type=int, required=True)
def send_debrief(dest: str):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--client', type=int, required=True)
@click.option('-s', '--script', type=str, required=True)
def simulate_call(client: str, cid: int, script: str):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--client', type=int, required=True)
@click.option('-f', '--format', type=str, required=True)
def get_report(client: str, cid: int, format: str):
  pass

@click.command()
@click.option('-c', '--client', type=str, required=True)
@click.option('-cid', '--client', type=int, required=True)
@click.option('-t', '--to', type=str, required=True)
def send_report(client: str, cid: int, to: str):
  pass
