import random
import string
import json
from calendar import isleap
from datetime import date, timedelta
from functools import reduce

from faker import Faker
from random import randint

fake = Faker()
Faker.seed(0)


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


class Task:
    complexity = None

    def __init__(self):
        self.data_list = self.get_data_list()
        self.solutions_list = self.get_solutions_list()

    def get_data_list(self):
        # data is stored in lists for each check to allow args unpacking
        data_list = []
        for i in range(5):
            data = self.get_data()
            if type(data) == tuple:
                data_list.append(data)
            else:
                data_list.append([data])
        return data_list

    def get_solutions_list(self):
        # Unpack each data list
        return [self.get_solution(*data) for data in self.data_list]

    def get_data(self):
        raise NotImplementedError

    def get_solution(self, *args):
        raise NotImplementedError

    @property
    def task(self):
        return "\n------ TASK ------\n"\
               f"TYPE: {self.type}\n\n" \
               f"TASK: {self._strip_doc()}\n\n" \
               f"REWARD: {self.complexity*2}\n"\
               "------------------\n"

    def _strip_doc(self):
        return ' '.join(self.__doc__.split())

    @property
    def type(self):
        return type(self).__name__


class Echo(Task):
    """
    Створіть функцію, яка приймає рядок і повертає його без змін.
    """
    complexity = 0

    def get_data(self): return fake.name()

    def get_solution(self, data): return data


class Increaser(Task):
    """
    Створіть функцію, яка приймає число і повертає число + 1
    """
    complexity = 1

    def get_data(self): return randint(-100, 100)

    def get_solution(self, n): return n+1


class HelloName(Task):
    """
    Створіть функцію, яка приймає ім'я і повертає 'Hello, {ім'я}!'.
    """
    complexity = 1

    def get_data(self): return fake.name()

    def get_solution(self, name): return f"Hello, {name}!"


class Sum(Task):
    """
    Створіть функцію, яка приймає два числа і повертає їх суму.
    """
    complexity = 1

    def get_data(self):
        return randint(-100, 100), randint(-100, 100)

    def get_solution(self, a, b): return a + b


class Difference(Task):
    """
    Створіть функцію, яка приймає два числа і повертає їх різницю.
    """
    complexity = 1

    def get_data(self):
        return randint(-100, 100), randint(-100, 100)

    def get_solution(self, a, b): return a - b


class Square(Task):
    """
    Напишіть функцію, яка приймає число і повертає його квадрат
    """
    complexity = 1

    def get_data(self): return randint(-100, 100)

    def get_solution(self, number): return number ** 2
    

class Perimeter(Task):
    """
    Створіть функцію, яка приймає довжину і шириту прямокутника,
    а повертає його периметр
    """
    complexity = 1
    
    def get_data(self): return randint(1, 100), randint(1, 100)

    def get_solution(self, a, b):
        return (a+b)*2


class SecondsInHour(Task):
    """
    Напишіть функцію, яка приймає число годин і повертає кількість секунд в них
    """
    complexity = 1

    def get_data(self): return randint(0, 10)

    def get_solution(self, n): return n * 60 * 60


class ConditionalSum(Task):
    """
    Створіть функцію, яка приймає два числа.
    Якщо перше число більше -- поверніть їх добуток.
    Якщо перше число менше -- поверніть їх різницю (a-b)
    """
    complexity = 2

    def get_data(self):
        return randint(-100, 100), randint(-100, 100)

    def get_solution(self, a, b):
        if a > b:
            return a * b
        return a - b


class GuessNumber(Task):
    """
    Створіть функцію, яка приймає два числа.
    Якщо числа рівні, поверніть "Equal".
    Якщо перше число більше від другого, поверніть "Bigger".
    Інакше поверніть "Smaller".
    """
    complexity = 2
    def get_data(self): return randint(-100, 100), randint(-100, 100)

    def get_solution(self, a, b):
        if a == b:
            return "Equal"
        elif a > b:
            return "Bigger"
        else:
            return "Smaller"


class HelloAnn(Task):
    """
    Створіть функцію, яка приймає ім'я.
    Якщо ім'я починається з 'A' -- поверніть 'Hello, {ім'я}!'
    Якщо ім'я починається з іншої літери -- поверніть 'Goodbye, {ім'я}!'
    """
    complexity = 2

    def get_data(self): return fake.name()

    def get_solution(self, name):
        if name[0] == 'A':
            return f'Hello, {name}!'
        return f'Goodbye, {name}!'


class CountLetter(Task):
    """
    Створіть функцію, яка приймає рядок і літеру.
    Поверніть число, скільки разів ця літера зустрічається в даному рядку.
    """
    complexity = 2

    def get_data(self):
        return fake.paragraph(), get_random_string(1)

    def get_solution(self, string, letter):
        counter = 0
        for i in string:
            if i == letter:
                counter += 1
        return counter


# class Modulo(Task):
#     task = "number: int -> modulo of number"
#     complexity = 1
#
#     def get_data(self):
#         return randint(-100, 100)
#
#     def get_solution(self, number):
#         return abs(number)
#
#


class FirstLetter(Task):
    """
    Напишіть функцію, яка примаймає рядок і повертає його першу літеру
    """
    complexity = 2

    def get_data(self): return fake.name()

    def get_solution(self, data): return data[0]


class LastLetter(Task):
    task = "name: str -> last letter of name"
    complexity = 1

    def get_data(self): return fake.name()

    def get_solution(self, data): return data[-1]

#
# class FirstTenLetters(Task):
#     task = "string: str -> first ten letters of string"
#     complexity = 1
#
#     def get_data(self):
#         return get_random_string(100)
#
#     def get_solution(self, data):
#         return data[:10]
#
#
# class Average(Task):
#     task = "numbers: list of int -> average of numbers"
#     complexity = 3
#
#     def get_data(self):
#         data = []
#         for _ in range(10):
#             data.append(randint(0, 100))
#         return data
#
#     def get_solution(self, data):
#         return sum(data)/len(data)
#
#
# class LastTenLetters(Task):
#     task = "string: str -> last ten letters of string"
#     complexity = 1
#
#     def get_data(self):
#         return get_random_string(100)
#
#     def get_solution(self, data):
#         return data[-10:]



# class Slice10To20(Task):
#     task = "Букви від 10 по 20"
#     complexity = 1
#
#     def get_data(self):
#         return get_random_string(100)
#
#     def get_solution(self):
#         return self.data[10:20]
#



# class FindLetter(Task):
#     complexity = 2
#
#     def __init__(self):
#         self.seed = get_random_string(1)
#         super().__init__()
#
#     @property
#     def task(self):
#         return f'Позиція першої букви {self.seed}'
#
#     def get_data(self):
#         return get_random_string(100)
#
#     def get_solution(self):
#         return self.data.find(self.seed)
#
#
# class FindNumber(Task):
#     task = 'Позиція цифри серед букв'
#     complexity = 2
#
#     def get_data(self):
#         string = get_random_string(100)
#         position = randint(0, 100)
#         return string[:position] + str(randint(0, 9)) + string[position:]
#
#     def get_solution(self):
#         for i in range(len(self.data)):
#             if self.data[i].isdigit():
#                 return i
#
#
# class FindLongestWord(Task):
#     task_description = 'Найдовше слово у тексті.'
#
#     def get_data(self):
#         return fake.sentence()
#
#     def get_solution(self):
#         words = self.data.split(' ')
#         longest = ''
#         for word in words:
#             if len(word) > len(longest):
#                 longest = word
#         return longest
#
#
# class SwapCases(Task):
#     task = 'Регістри всіх літер змінені місцями.'
#     complexity = 2
#
#     def get_data(self):
#         return get_random_string(1000)
#
#     def get_solution(self):
#         return ''.join([l.upper() if l.islower() else l.lower() for l in self.data])
#
#
# class AlphabeticOrder(Task):
#     task = 'Переставити букви в алфівітному порядку.'
#
#     def get_data(self):
#         return get_random_string(100)
#
#     def get_solution(self):
#         return ''.join(sorted(self.data))
#
#
# class ReverseString(Task):
#     task = 'Дані в зворотньому порядку.'
#     complexity = 2
#
#     def get_data(self):
#         return get_random_string(100)
#
#     def get_solution(self):
#         return self.data[::-1]
#
#
# class ChangeKeysValues(Task):
#     task = 'Змінити ключі і значення місцями, наприклад {1:2, 3:4} -> {2:1, 4:3}'
#     complexity = 3
#
#     def get_data(self):
#         new_dict = {}
#         for i in range(50):
#             new_dict.update({get_random_string(3): get_random_string(3)})
#         return new_dict
#
#     def get_solution(self):
#         return {value: key for key, value in self.data.items()}
#
#
# class ReverseText(Task):
#     task = 'Кожне слово задом наперед.'
#     complexity = 2
#
#     def get_data(self):
#         return fake.sentence()
#
#     def get_solution(self):
#         new_words = []
#         for word in self.data.split(' '):
#             new_words.append(word[::-1])
#         return ' '.join(new_words)
#
