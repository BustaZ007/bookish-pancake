import json
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from sqlalchemy import Integer, String, Column, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///sqlite_python.db")
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

app = FastAPI()


class SneakerFastApi(BaseModel):
    name: str
    count: int
    price: int
    size: str
    creator: str

    class Config:
        orm_mode = True


class Sneaker(Base):
    __tablename__ = 'sneakers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False, default=1)
    price = Column(Integer, nullable=False)
    size = Column(String(100), nullable=False)
    creator = Column(String(100), nullable=False)

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

    def add_sneaker(self, name, price, count, creator, size):
        return self._dbservices.add_sneaker(Sneaker(name, price, count, creator, size))

    def delete_sneaker(self, name):
        return self._dbservices.delete_sneaker_by_name(name)

    def display_sneakers(self):
        sneakers = self._dbservices.get_sneakers()
        if len(sneakers) == 0:
            return 'Sneakers list is empty'

        return sneakers

    def read_sneakers_from_file(self):
        with open('read.json', 'r') as file:
            sneakers_dict = json.load(file)
            for sneaker in sneakers_dict['sneakers']:
                self._dbservices.add_sneaker(
                    Sneaker(sneaker['name'], sneaker['price'], sneaker['count'], sneaker['creator'], sneaker['size'])
                )


class DBServices:
    def add_sneaker(self, sneaker):
        try:
            count_products = session.query(Sneaker.count).filter(Sneaker.name == sneaker.name).one_or_none()
            if count_products is not None:
                session.query(Sneaker).filter(Sneaker.name == sneaker.name). \
                    update({"count_products": count_products[0] + sneaker.count_products}, synchronize_session="fetch")
            else:
                session.add(sneaker)
            session.commit()

            return True

        except Exception as error:
            return error

    def delete_sneaker_by_name(self, name):
        try:
            session.query(Sneaker).filter(Sneaker.name == name) \
                .delete(synchronize_session="fetch")

            session.commit()
            return True
        except Exception as error:
            print(error)
            return False

    def get_sneakers(self):
        try:
            return session.query(Sneaker).all()
        except Exception as error:
            print(error)


sneakers_service = SneakersService()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/getAllSneakers")
async def get_all_sneakers():
    return sneakers_service.display_sneakers()


@app.post("/addSneaker")
async def add_sneaker(sneaker: SneakerFastApi):
    return sneakers_service.add_sneaker(sneaker.name, sneaker.price, sneaker.count, sneaker.creator, sneaker.size)


@app.delete("/deleteSneakerByName/{name}")
async def delete_sneaker_by_id(name):
    return sneakers_service.delete_sneaker(name)


# while (True):
#     print('1 - Add sneaker')
#     print('2 - Delete sneaker')sneaker.
#     print('3 - Display all sneakers')
#     print('4 - Add sneakers from file')
#     print('5 - Exit')
#     command = input('Input command number: ')
#     if command == '1':
#         name = input('Input sneaker name: ')
#         price = int(input('Input sneaker price: '))
#         while price < 0:
#             price = int(input('Incorrect price value, please try again: '))
#         count = int(input('Input sneaker count: '))
#         while count < 1:
#             count = int(input('Incorrect count value, please try again: '))
#         creator = input('Input sneaker creator: ')
#         size = input('Input sneaker size: ')
#         sneakers_service.add_sneaker(name, price, count, creator, size)
#     elif command == '2':
#         name = input('Input sneaker name for deleting: ')
#         sneakers_service.delete_sneaker(name)
#     elif command == '3':
#         sneakers_service.display_sneakers()
#     elif command == '4':
#         sneakers_service.read_sneakers_from_file()
#     elif command == '5':
#         break
#     else:
#         print('Unknown command, please try again')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
