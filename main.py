# cd /home/ekaterina/PycharmProjects/calendar
# python3 main.py
# python3 main.py add_person -n Kate -s Okman -d 08-12-1996

import click
import json
import datetime
import uuid
import os
from pathlib import Path
from collections import namedtuple
from prettytable import PrettyTable

class Person(object):
    def __init__(self, name, surname, dob):
        self.id = uuid.uuid4().hex
        self.name = name
        self.surname = surname
        self.dob = dob

    def __eq__(self, other):
        return self.name == other.name and self.surname == other.surname and \
               self.dob == other.dob

    def to_dict(self):
        dict_of_person = {'id': self.id, 'name': self.name, 'surname': self.surname, 'dob': self.dob}
        return dict_of_person

class PersonList(object):
    def __init__(self, storage):
        self.data = storage.read()
        self.storage = storage
        self.counter = -1
        self.data_of_person = self.from_dict()
        self.index = len(self.data)

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter <= (len(self) - 2):
            self.counter += 1
            return self.data_of_person[self.counter]  #возвращается объект
        else:
            raise StopIteration

    def append(self, new_person):
        self.data.append(new_person.to_dict())
        return self.data

    def save(self):
        self.storage.write(self.data)

    def from_dict(self):
        self.data_of_person = []
        for i in self.data:
            d_named = namedtuple("Person", i.keys())(*i.values())
            person_from_dict = Person(d_named.name, d_named.surname, d_named.dob)
            self.data_of_person.append(person_from_dict)
        return self.data_of_person                        #возвращаем список объектов Person


class FileStorage(object):
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            self.create()

    def read(self):
        with open(self.path, 'r') as myfile:
            data_json = json.loads(myfile.read())
            return data_json

    def write(self, data):
        with open(self.path, 'w') as myfile:
            json.dump(data, myfile)

    def create(self):
        with open(self.path, 'tw') as myfile:
            myfile.write('[]')

    @classmethod
    def home_dir(cls):
        home_dir = str(Path.home())
        full_path = os.path.join(home_dir, 'store.txt')
        return cls(full_path)

class Table(object):
    def __init__(self):
        self.x = PrettyTable()
        self.x.field_names = ["Id", "Name", "Surname", "Dob"]

    def get_table(self):
        print(self.x)

    def add_row(self, i):
        self.x.add_row([i['id'], i['name'], i['surname'], i['dob']])

file = FileStorage.home_dir()
person_list = PersonList(file)

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
    person = Person(name, surname, dob)
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
    table = Table()
    for i in person_list.data:
        table.add_row(i)
    table.get_table()

@click.command()
@click.option('--name', '-n', help='Enter the name of person you want to find')
def search(name):
    name = name.capitalize()
    table = Table()
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
    table = Table()
    count = 0
    for i in person_list.data:
        if month == i['dob'][3:5]:
            count += 1
            table.add_row(i)
    if count >= 1:
        table.get_table()
    else:
        raise Exception("Person happy birthday this month is not on the list")


cli.add_command(add)
cli.add_command(delete)
cli.add_command(list_full)
cli.add_command(search)
cli.add_command(search_month)


if __name__ == '__main__':
    cli()




