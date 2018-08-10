from . import models
import click

def init_person_list():
    file_storage = models.FileStorage.home_dir()
    person_list = models.PersonList(file_storage)
    return person_list

@click.group()
def cli():
    pass

@click.command()
@click.option('--name', '-n', help='Enter name')
@click.option('--surname', '-s', help='Enter surname')
@click.option('--dob', '-d', help='The date of birth format "dd-mm-yyyy"')
def add(name, surname, dob):
    person_list = init_person_list()
    name = name.capitalize()
    surname = surname.capitalize()
    person = models.Person(name, surname, dob)
    if person in person_list:
        raise Exception("Person already exist")
    else:
        person_list.append(person)
        person_list.save()

@click.command()
@click.option('--id_of_person', '-i', help='Enter the id of the person you want to delete')
def delete(id_of_person):
    person_list = init_person_list()
    person_list.delete_person(id_of_person)
    person_list.save()


@click.command()
def list_full():
    person_list = init_person_list()
    person_list.show(output_format='table')

@click.command()
@click.option('--name', '-n', help='Enter the name of person you want to find')
def search(name):
    person_list = init_person_list()
    name = name.capitalize()
    person_list.search_by_name(name)
    person_list.show(output_format='table')

@click.command()
@click.option('--month', '-m', help='Enter your birth month to search')
def search_month(month):
    person_list = init_person_list()
    person_list.search_by_month(month)
    person_list.show(output_format='table')
