# cd /home/ekaterina/PycharmProjects/calendar/app
# python3 main.py
# python3 main.py add_person -n Kate -s Okman -d 08-12-1996

# import app.commands as commands
from . import commands

commands.cli.add_command(commands.add)
commands.cli.add_command(commands.delete)
commands.cli.add_command(commands.list_full)
commands.cli.add_command(commands.search)
commands.cli.add_command(commands.search_month)


if __name__ == '__main__':
    commands.cli()




