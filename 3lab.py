import random
from datetime import datetime
from threading import Thread


def write(number):
    file = open("./test/" + str(number) + "text.txt", "w")
    for string_number in range(random.randint(20, 100)):
        for number in range(random.randint(5, 40)):
            file.write(str(random.randint(0, 9)))

        file.write('\n')

    file.close()


def read(number):
    file = open("./test/" + str(number) + "text.txt", "r")
    text = file.read().replace("\n", '')
    res = 0
    for i in text:
        res = res + int(i)
    file.close()

    return res


def get_result(n):
    for i in range(n, n + 1000):
        write(i)

    for i in range(n, n + 1000):
        print(f"Файл №{i} - Содержание файла: {read(i)}")


start_time = datetime.now()

my_thread1 = Thread(target=get_result, args=(0,))
my_thread2 = Thread(target=get_result, args=(1000,))

my_thread1.start()
my_thread2.start()
#
my_thread1.join()
my_thread2.join()


print(datetime.now() - start_time)