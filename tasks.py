import random
import string
from calendar import isleap
from datetime import date, timedelta


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


def get_random_year():
    start, end = date(1900, 1, 1), date(2020, 2, 1)
    days_between_dates = (end - start).days
    return (start + timedelta(days=random.randrange(days_between_dates))).year


class Task:
    task = str()
    complexity = 10

    def __init__(self):
        self.data = self.get_data()
        self.solution = self.get_solution()

    def get_data(self):
        raise NotImplementedError

    def get_solution(self):
        raise NotImplementedError


class GoodbyeWorld(Task):
    task = "Прислати \"Goodbye World\""
    complexity = 0

    def get_data(self):
        return ""

    def get_solution(self):
        return "Goodbye World"


class HelloWorld(Task):
    task = "Прислати \"Hello World\""
    complexity = 0

    def get_data(self):
        return ""

    def get_solution(self):
        return "Hello World"


class Echo(Task):
    task = "Дані, як вони є"
    complexity = 0

    def get_data(self):
        return get_random_string(100)

    def get_solution(self):
        return self.data


class FirstLetter(Task):
    task = "Перша буква"
    complexity = 1

    def get_data(self):
        return get_random_string(100)

    def get_solution(self):
        return self.data[0]


class LastLetter(Task):
    task = "Остання буква"
    complexity = 1

    def get_data(self):
        return get_random_string(100)

    def get_solution(self):
        return self.data[-1]


class FirstTenLetters(Task):
    task = "Перші 10 букв"
    complexity = 1

    def get_data(self):
        return get_random_string(100)

    def get_solution(self):
        return self.data[:10]


class LastTenLetters(Task):
    task = "Останні 10 букв"
    complexity = 1

    def get_data(self):
        return get_random_string(100)

    def get_solution(self):
        return self.data[-10:]


class Slice10To20(Task):
    task = "Букви від 10 по 20"
    complexity = 1

    def get_data(self):
        return get_random_string(100)

    def get_solution(self):
        return self.data[10:20]


class CountLetters(Task):
    complexity = 2

    def __init__(self):
        self.seed = get_random_string(1).lower()
        super().__init__()

    @property
    def task(self):
        return f'Кількість літер {self.seed}'

    def get_data(self):
        return get_random_string(200)

    def get_solution(self):
        return self.data.count(self.seed)


class FindLetter(Task):
    complexity = 2

    def __init__(self):
        self.seed = get_random_string(1)
        super().__init__()

    @property
    def task(self):
        return f'Позиція першої букви {self.seed}'

    def get_data(self):
        return get_random_string(100)

    def get_solution(self):
        return self.data.find(self.seed)


class FindNumber(Task):
    task = 'Позиція цифри серед букв'
    complexity = 2

    def get_data(self):
        string = get_random_string(100)
        position = random.randint(0, 100)
        return string[:position] + str(random.randint(0, 9)) + string[position:]

    def get_solution(self):
        for i in range(len(self.data)):
            if self.data[i].isdigit():
                return i


# class FindLongestWord(Task):
#     task_description = 'Найдовше слово у тексті.'
#
#     def get_data(self):
#         return factory.Faker('sentence', nb_words=100).generate()
#
#     def get_solution(self):
#         words = self.body.split(' ')
#         longest = ''
#         for word in words:
#             if len(word) > len(longest):
#                 longest = word
#         return longest


class SwapCases(Task):
    task = 'Регістри всіх літер змінені місцями.'
    complexity = 2

    def get_data(self):
        return get_random_string(1000)

    def get_solution(self):
        return ''.join([l.upper() if l.islower() else l.lower() for l in self.data])


class AlphabeticOrder(Task):
    task = 'Переставити букви в алфівітному порядку.'

    def get_data(self):
        return get_random_string(100)

    def get_solution(self):
        return ''.join(sorted(self.data))


class ReverseString(Task):
    task = 'Дані в зворотньому порядку.'
    complexity = 2

    def get_data(self):
        return get_random_string(100)

    def get_solution(self):
        return self.data[::-1]


class ChangeKeysValues(Task):
    task = 'Змінити ключі і значення місцями, наприклад {1:2, 3:4} -> {2:1, 4:3}'
    complexity = 3

    def get_data(self):
        new_dict = {}
        for i in range(50):
            new_dict.update({random.randint(0, 1000): random.randint(0, 1000)})
        return new_dict

    def get_solution(self):
        return {value: key for key, value in self.get_data().items()}


# class ReverseText(Gem):
#     def get_task(self):
#         return 'Кожне слово задом наперед.'
#
#     def get_body(self):
#         return factory.Faker('sentence', nb_words=100).generate()[:-1]
#
#     def get_solution(self):
#         new_words = []
#         for word in self.body.split(' '):
#             new_words.append(word[::-1])
#         return ' '.join(new_words)


class IsYearLeap(Task):
    task = 'Проверить, является ли год високосным.'
    complexity = 3

    def get_data(self):
        return get_random_year()

    def get_solution(self):
        return isleap(self.data)


# class CountWords(Task):
#     task = 'Для каждого слова из данного текста подсчитайте, сколько раз оно встречалось в этом тексте.'
#     complexity = 3
#
#     def get_data(self):
#         return get_random_year()
#
#     def get_solution(self):
#         return isleap(self.data)
