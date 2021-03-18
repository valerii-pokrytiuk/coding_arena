from redis import Redis

redis = Redis(host='localhost', port=6379, db=0, decode_responses=True)

def move(movestr):
    x = 0
    y = 0
    step = 10
    for i in movestr:
        if i == 'u':
            y += step
        elif i == 'r':
            x += step
        elif i == 'd':
            y -= step
        elif i == 'l':
            x -= step
        else:
            ...
    redis.publish(
        'game-commands',
        f"-move {x} {y} 1"
    )
    
def map():
    redis.publish(
        'game-commands',
        '-map'
        )