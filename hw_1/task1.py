import click
import sys


def order_difference(a: int, b: int) -> int:
    if a < 1 or b < 1:
        return 0
    return len(str(b)) - len(str(a))

@click.command()
@click.argument('file', type=click.File('r'), required=False)
def nl(file):

    if file is None:
        file =  sys.stdin.readlines()
        click.echo()
    else:
        file = file.readlines()

    line_number = 1
    for line in file:
        spaces = ' ' * order_difference(line_number, len(file))
        click.echo(f"    {spaces}{line_number}  {line.rstrip()}")
        line_number += 1

if __name__ == '__main__':
    nl()