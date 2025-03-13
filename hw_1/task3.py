import click
import sys
import io

from dataclasses import dataclass


@dataclass
class WCParametrs():
    count_lines: int
    count_words: int
    count_bytes: int

def count_params(file) -> WCParametrs:
    lines = file.readlines()
    count_lines = len(lines) - 1
    count_words = sum([len(line.split()) for line in lines])
    file.seek(0)
    count_bytes = len(file.read())
    return WCParametrs(count_lines, count_words, count_bytes)

@click.command()
@click.argument('files', nargs=-1, type=click.File('rb'))
def wc(files):
    if not files:
        content = sys.stdin.read()
        lines = io.StringIO(content)
        parametrs: WCParametrs = count_params(lines)
        click.echo()
        click.echo(f'{' ' * (len(str(parametrs.count_words)) - 1)}{parametrs.count_lines}{' ' * len(str(parametrs.count_words))}{parametrs.count_words} {parametrs.count_bytes}')
        return
    
    buffer = WCParametrs(0, 0, 0)
    for file in files:
        
        parametrs: WCParametrs =count_params(file)
        click.echo(f'{' ' * (len(str(parametrs.count_words)) - 1)}{parametrs.count_lines:}{' ' * len(str(parametrs.count_words))}{parametrs.count_words} {parametrs.count_bytes} {file.name}')
        
        if len(files) > 1:
            buffer.count_bytes += parametrs.count_bytes
            buffer.count_words += parametrs.count_words
            buffer.count_lines += parametrs.count_lines


    if len(files) > 1:
        click.echo(f'{' ' * (len(str(parametrs.count_words)) - 1)}{buffer.count_lines}{' ' * len(str(buffer.count_words))}{buffer.count_words} {buffer.count_bytes} total')

if __name__ == '__main__':
    wc()