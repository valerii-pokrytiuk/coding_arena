from client import Gateway

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

def increaser(x):
    """Increaser"""
    return x + 1

def summator(a, b):
    return a+b

def square(a):
    """Square"""
    return a**2

def rectangle(a, b):
    """Perimeter"""
    return (a+b)*2

def hello(a):
    """HelloName"""
    return f'Hello, {a}!'

def count_seconds(s):
    """SecondsInHour"""
    return s*60*60

def echo(s):
    """Echo"""
    return s

def diff(a, b):
    """Difference"""
    return a - b

def cond_sum(a, b):
    """ConditionalSum"""
    if a > b:
        return a*b
    return a - b

def test(a, b):
    """GuessNumber"""
    return a

def hello_ann(a):
    """HelloAnn"""
    if a[0] == 'A':
        return hello(a)
    return f'Goodbye, {a}!'


gate.check()
gate.task()
