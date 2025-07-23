import click
from app.services import power, fibonacci, factorial

@click.group()
def cli():
    """Math Service CLI for performing calculations."""
    pass

@cli.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
def power_cmd(a,b):
    click.echo(f"Power of {a} raised to {b} is: {power(a, b)}")

@cli.command()
@click.argument('n', type=int)
def fibonacci_cmd(n):
    click.echo(f"The {n}th Fibonacci number is: {fibonacci(n)}")


@cli.command()
@click.argument('n', type=int)
def factorial_cmd(n):
    click.echo(f"The factorial of {n} is: {factorial(n)}")

if __name__ == '__main__':
    cli()

#For testing purposes, you can run this script directly. Later GUI implementation will replace this CLI.
# To run the CLI, use the command: python cli.py <command> <arguments>