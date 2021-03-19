from client import Gateway, solve

gate = Gateway('blue')

def move(movestr):
    step = 5
    x = 0
    y = 0
    for i in movestr:
        if i == 'u':
            y += step
        elif i == 'r':
            x += step
        elif i == 'd':
            y -= step
        elif i == 'l':
            x -= step
    gate.move(x, y)

@solve("Increaser")
def increaser(x):
    return x + 1

def summator(a, b):
    return a+b

@solve('Square')
def square(a):
    return a**2

@solve('Perimeter')
def rectangle(a, b):
    return (a+b)*2

@solve('HelloName')
def hello(a):
    return f'Hello, {a}!'

@solve('SecondsInHour')
def count_seconds(s):
    return s*60*60

@solve('Echo')
def echo(s):
    return s

@solve('Difference')
def diff(a, b):
    return a - b

@solve('ConditionalSum')
def cond_sum(a, b):
    if a > b:
        return a*b
    return a - b

@solve('GuessNumber')
def test(a, b):
    return a

@solve('HelloAnn')
def hello_ann(a):
    if a[0] == 'A':
        return hello(a)
    return f'Goodbye, {a}!'


gate.check()
gate.task()
