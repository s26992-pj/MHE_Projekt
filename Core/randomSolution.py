import random

def randomSolution(numbers):
    return random.sample(numbers, random.randint(1,len(numbers)))