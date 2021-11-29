import json


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
            "name" : self.name,
            "price" : self.price,
            "count" : self.count,
            "creator" : self.creator,
            "size" : self.size
        }


class SneakersService:
    def __init__(self):
        self._sneakers = []

    def add_sneaker(self, name, price, count, creator, size):
        self._sneakers.append(Sneaker(name, price, count, creator, size))

    def delete_sneaker(self, name):
        delete_sneaker = None
        for sneaker in self._sneakers:
            if sneaker.name == name:
                self._sneakers.remove(sneaker)
                delete_sneaker = sneaker
        return delete_sneaker is None

    def display_sneakers(self):
        if len(self._sneakers) == 0:
            print('Sneakers list is empty \n')
            return
        for sneaker in self._sneakers:
            print(str(sneaker) + '\n')

    def read_sneakers_from_file(self):
        with open('read.json', 'r') as file:
            sneakers_dict = json.load(file)
            self._sneakers.extend(sneakers_dict['sneakers'])

    def save(self):
        sneakers_list_json = []
        for sneaker in self._sneakers:
            sneakers_list_json.append(sneaker.to_json())
        with open('test.json', 'w') as file:
            json.dump({"sneakers":sneakers_list_json}, file)

    def backup(self):
        with open('test.json', 'r') as file:
            sneakers_dict = json.load(file)
            self._sneakers = sneakers_dict['sneakers']


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
        sneakers_service.save()
        break
    else:
        print('Unknown command, please try again')
