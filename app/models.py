import json
import uuid
import os
import datetime
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
            return self.data_of_person[self.counter]
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
        return self.data_of_person

    def show(self, output_format):
        if output_format == 'table':
            table = Table()
            for i in self.data:
                table.add_row(i)
            table.get_table()

    def search_by_name(self, name):
        list_of_names = []
        for i in self.data:
            if name in i['name']:
                list_of_names.append(i)
        self.data = list_of_names

        if len(list_of_names) >= 1:
            return self.data
        else:
            raise Exception("Person with this name is not on the list.")

    def delete_person(self, id_of_person):
        count_id = 0
        del_i = 0
        for i in self.data:
            if id_of_person in i['id'] and id_of_person[0:3] == i['id'][0:3]:
                count_id += 1
                del_i = i
                if count_id >= 2:
                    raise Exception("Id is repeated")
        if count_id == 0:
            raise Exception("There is no person with this id in the list")
        else:
            self.data.remove(del_i)
            return self.data
    def search_by_month(self, month):
        list_of_month = []
        for i in self.data:
            dob = datetime.datetime.strptime(i['dob'], '%d-%m-%Y')
            if int(month) == dob.month:
                list_of_month.append(i)
        if len(list_of_month) >= 1:
            self.data = list_of_month
            return self.data
        else:
            raise Exception("Person happy birthday this month is not on the list")


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