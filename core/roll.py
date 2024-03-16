from random import randint

def roll(roll):
    rolling = []
    try:
        for x in range(int(roll.split('d')[0])):
            rolling.append(randint(1,int(roll.split('d')[1])))
        total = sum(rolling)
        return total, rolling
    except Exception as err:
        return None, str(err)
