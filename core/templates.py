import click

@click.command()
@click.option('t', '--name', type=str, required=True, help="Name of the template for identification")
@click.option('-d', '--difficulty', type=str, required=True, help="Difficulty of template")
def create_template():
  pass