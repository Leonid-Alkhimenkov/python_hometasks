import sys
import click


@click.command()
@click.argument('files', nargs=-1, type=click.File('r'))
def tail(files):
    if not files:
        lines = sys.stdin.readlines()
        last_lines = lines[-17:] if len(lines) >= 17 else lines
        click.echo()
        for line in last_lines:
            click.echo(line.rstrip())
        return
    
    for file in files:
        if len(files) > 1:
            click.echo(f"==> {file.name} <==")
        
        lines = file.readlines()
        
        last_lines = lines[-10:] if len(lines) > 9 else lines
        
        for line in last_lines:
            click.echo(line.rstrip())

if __name__ == '__main__':
    tail()