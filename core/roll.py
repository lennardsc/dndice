from random import randint

def roll(roll):
    rolling = []
    try:
        for x in range(int(roll.split('d')[0])):
            rolling.append(randint(1,int(roll.split('d')[1])))
    except Exception as err:
        print(f'i got @_@ \n Error: {err}')
    print(f'You rolled {"".join(str(x)for x in rolling)}which has a total'
        f' of {sum(rolling)}')
