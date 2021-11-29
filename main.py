import json
import sqlite3


class Sneaker:
    def __init__(self, name, price, count, creator, size):
        self.name = name
        self.price = price
        self.count = count
        self.creator = creator
        self.size = size

    def __str__(self):
        return self.name + ' ' + str(self.price) + ' ' + str(self.count) + ' ' + self.creator + ' ' + str(self.size)

    def to_json(self):
        return {
            "name": self.name,
            "price": self.price,
            "count": self.count,
            "creator": self.creator,
            "size": self.size
        }


class SneakersService:
    def __init__(self):
        self._sneakers = []
        self._dbservices = DBServices()
        self._dbservices.create_table()

    def add_sneaker(self, name, price, count, creator, size):
        self._dbservices.add_sneaker(Sneaker(name, price, count, creator, size))

    def delete_sneaker(self, name):
        self._dbservices.delete_sneaker(name)

    def display_sneakers(self):
        sneakers = self._dbservices.get_sneakers()
        if len(sneakers) == 0:
            print('Sneakers list is empty')
            return
        for sneaker in sneakers:
            print(str(sneaker))

    def read_sneakers_from_file(self):
        with open('read.json', 'r') as file:
            sneakers_dict = json.load(file)
            for sneaker in sneakers_dict['sneakers']:
                self._dbservices.add_sneaker(
                    Sneaker(sneaker['name'], sneaker['price'], sneaker['count'], sneaker['creator'], sneaker['size'])
                )


class DBServices:
    def create_table(self):
        try:
            sqlite_connection = sqlite3.connect('sqlite_python.db')
            cursor = sqlite_connection.cursor()
            sqlite_create_table_query = '''CREATE TABLE sneakers (
                                            id INTEGER PRIMARY KEY,
                                            Name TEXT NOT NULL,
                                            Price INTEGER NOT NULL,
                                            Count INTEGER NOT NULL,
                                            Creator TEXT NOT NULL,
                                            Size TEXT NOT NULL);'''
            cursor.execute(sqlite_create_table_query)
            sqlite_connection.commit()
            cursor.close()
            sqlite_connection.close()
        except sqlite3.Error as error:
            print(error)

    def add_sneaker(self, sneaker):
        try:
            sqlite_connection = sqlite3.connect('sqlite_python.db')
            cursor = sqlite_connection.cursor()
            sqlite_insert_query = f"""INSERT INTO sneakers
                                              (Name , Price, Count, Creator, Size)  
                                              VALUES  ("{sneaker.name}", {sneaker.price}, {sneaker.count},
                                              "{sneaker.creator}", "{sneaker.size}")"""
            cursor.execute(sqlite_insert_query)
            sqlite_connection.commit()
            cursor.close()
            sqlite_connection.close()
        except sqlite3.Error as error:
            print(error)

    def delete_sneaker(self, name):
        try:
            sqlite_connection = sqlite3.connect('sqlite_python.db')
            cursor = sqlite_connection.cursor()
            sqlite_insert_query = f"""DELETE from sneakers where name = {name}"""
            cursor.execute(sqlite_insert_query)
            sqlite_connection.commit()
            cursor.close()
            sqlite_connection.close()
        except sqlite3.Error as error:
            print(error)

    def get_sneakers(self):
        try:
            sqlite_connection = sqlite3.connect('sqlite_python.db')
            cursor = sqlite_connection.cursor()
            sqlite_insert_query = """select * from sneakers"""
            cursor.execute(sqlite_insert_query)
            result = cursor.fetchall()
            cursor.close()
            sqlite_connection.close()
            return result
        except sqlite3.Error as error:
            print(error)


sneakers_service = SneakersService()
while(True):
    print('1 - Add sneaker')
    print('2 - Delete sneaker')
    print('3 - Display all sneakers')
    print('4 - Add sneakers from file')
    print('5 - Exit')
    command = input('Input command number: ')
    if command == '1':
        name = input('Input sneaker name: ')
        price = int(input('Input sneaker price: '))
        while price < 0:
            price =  int(input('Incorrect price value, please try again: '))
        count = int(input('Input sneaker count: '))
        while count < 1:
            count = int(input('Incorrect count value, please try again: '))
        creator = input('Input sneaker creator: ')
        size = input('Input sneaker size: ')
        sneakers_service.add_sneaker(name, price, count, creator, size)
    elif command == '2':
        name = input('Input sneaker name for deleting: ')
        sneakers_service.delete_sneaker(name)
    elif command == '3':
        sneakers_service.display_sneakers()
    elif command == '4':
        sneakers_service.read_sneakers_from_file()
    elif command == '5':
        break
    else:
        print('Unknown command, please try again')
