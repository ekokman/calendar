# cd /home/ekaterina/PycharmProjects/calendar/app
# python3 -m app.main
# python3 -m app.main -n Kate -s Okman -d 08-12-1989

from . import commands

commands.cli.add_command(commands.add)
commands.cli.add_command(commands.delete)
commands.cli.add_command(commands.list_full)
commands.cli.add_command(commands.search)
commands.cli.add_command(commands.search_month)


if __name__ == '__main__':
    commands.cli()




