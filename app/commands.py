from . import models
import click

file = models.FileStorage.home_dir()
person_list = models.PersonList(file)

@click.group()
def cli():
    pass

@click.command()
@click.option('--name', '-n', help='Enter name')
@click.option('--surname', '-s', help='Enter surname')
@click.option('--dob', '-d', help='The date of birth format "dd-mm-yyyy"')
def add(name, surname, dob):
    name = name.capitalize()
    surname = surname.capitalize()
    person = models.Person(name, surname, dob)
    if person in person_list:
        raise Exception("Person already exist")
    else:
        person_list.append(person)
        person_list.save()

@click.command()
@click.option('--id', '-i', help='Enter the id of the person you want to delete')
def delete(id):
    count_id = 0
    for i in person_list.data:
        if id in i['id'] and id[0:3] == i['id'][0:3]:
            count_id += 1
            del_i = i
            if count_id >= 2:
                raise Exception("Id is repeated")
    if count_id == 0:
        raise Exception("There is no person with this id in the list")
    else:
        person_list.data.remove(del_i)
        person_list.save()

@click.command()
def list_full():
    table = models.Table()
    for i in person_list.data:
        table.add_row(i)
    table.get_table()

@click.command()
@click.option('--name', '-n', help='Enter the name of person you want to find')
def search(name):
    name = name.capitalize()
    table = models.Table()
    count_name = 0
    for i in person_list.data:
        if name in i['name']:
            count_name += 1
            table.add_row(i)
    if count_name >= 1:
        table.get_table()
    else:
        raise Exception("Person with this name is not on the list.")

@click.command()
@click.option('--month', '-m', help='Enter the name of person you want to find')
def search_month(month):
    table = models.Table()
    count = 0
    for i in person_list.data:
        if month == i['dob'][3:5]:
            count += 1
            table.add_row(i)
    if count >= 1:
        table.get_table()
    else:
        raise Exception("Person happy birthday this month is not on the list")