from random import randint

def roll(roll):
    try:
        num_dice, num_sides = map(int, roll.split('d'))
        if num_dice <= 0 or num_sides <= 0:
            raise ValueError("Number of dice and number of sides must be positive integers")

        rolling = [randint(1, num_sides) for _ in range(num_dice)]
        total = sum(rolling)
        return total, rolling
    except ValueError as err:
        return None, f"Invalid roll format: {err}"
    except Exception as err:
        return None, str(err)
