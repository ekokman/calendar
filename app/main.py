from .commands import cli, add, delete, list_full, search_month, search

cli.add_command(add)
cli.add_command(delete)
cli.add_command(list_full)
cli.add_command(search)
cli.add_command(search_month)

if __name__ == '__main__':
    cli()