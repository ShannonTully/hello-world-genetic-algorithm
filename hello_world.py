"""This program will print 'Hello World!' using a genetic algorithm."""

import random
import timeit
import string


def fitness(guess):
    """Determine the fitness score of an individual."""
    if guess == 'Hello World!':
        return 'Done!'

    i = 0
    try:
        score = 0
        for i in range(len('Hello World!')):
            if guess[i] == 'Hello World!'[i]:
                score += 1
    except IndexError:
        score = 0
        for i in range(len(guess)):
            if guess[i] == 'Hello World!'[i]:
                score += 1

    return score - abs(len(guess) - len('Hello World!'))


def first_gen():
    """Generate the first population."""
    i = 0
    population = []

    for i in range(100):
        population.append(
            ''.join(
                random.choice(
                    string.ascii_letters + string.digits + '! '
                ) for _ in range(random.randint(1, 100))))

    return population


def calculate_fitness_of_population(population):
    """Take in a population and return them with their scores."""
    pop_with_fitness = []

    for individual in population:
        fit = fitness(individual)
        if fit == 'Done!':
            return fit
        pop_with_fitness.append([individual, fit])

    return pop_with_fitness


def new_breeders(pop_with_fitness):
    """Take in pop with fitness and return breeding population."""
    sorted_pop = quicksort(pop_with_fitness)
    breeders = []

    i = 0
    for i in range(99, 74, -1):
        try:
            breeders.append(sorted_pop[i])
        except IndexError:
            pass
    weights = [int((2 / x) * 100) for x in range(1, 51)]
    extras = [random.choices(sorted_pop[-50:], weights)[0] for _ in range(25)]
    breeders.extend(extras)
    return breeders


def breed(breeders):
    """Take in breeders and return new pop."""
    new_pop = []

    i = 0
    for i in range(50):
        if len(breeders) > 1:
            parents = [0, 0]
            child1 = ''
            child2 = ''
            child3 = ''
            child4 = ''
            parents[0] = random.choice(breeders)
            breeders.remove(parents[0])
            parents[1] = random.choice(breeders)
            breeders.remove(parents[1])
            if len(parents[0][0]) > len(parents[1][0]):
                parents[0], parents[1] = parents[1], parents[0]
            for j in range(len(parents[0][0])):
                    try:
                        if random.randint(0, 100) < 50:
                            child1 += str(parents[0][0][j])
                        else:
                            child1 += str(parents[1][0][j])
                    except IndexError:
                        try:
                            child1 += str(parents[1][0][j])
                        except IndexError:
                            pass
                    try:
                        if random.randint(0, 100) < 50:
                            child2 += str(parents[0][0][j])
                        else:
                            child2 += str(parents[1][0][j])
                    except IndexError:
                        try:
                            child2 += str(parents[1][0][j])
                        except IndexError:
                            pass
                    try:
                        if random.randint(0, 100) < 50:
                            child3 += str(parents[0][0][j])
                        else:
                            child3 += str(parents[1][0][j])
                    except IndexError:
                        try:
                            child3 += str(parents[1][0][j])
                        except IndexError:
                            pass
                    try:
                        if random.randint(0, 100) < 50:
                            child4 += str(parents[0][0][j])
                        else:
                            child4 += str(parents[1][0][j])
                    except IndexError:
                        try:
                            child4 += str(parents[1][0][j])
                        except IndexError:
                            pass
            if child1:
                new_pop.append(child1)
            if child2:
                new_pop.append(child2)
            if child3:
                new_pop.append(child3)
            if child4:
                new_pop.append(child3)
    return new_pop


def mutate(individual):
    """Take in a string and change it."""
    mutated = []
    new = individual
    # percentage = float(random.randint(0, 2)) / 10.0
    # if percentage < 1:
    # percentage = 1
    # for each in range(int(len(individual) * percentage)):
    mutated.append(random.randint(0, len(individual)))
    for index in mutated:
        while new == individual:
            other = random.randint(1, 4)
            if other == 1:
                temp = [c for c in individual]
                try:
                    temp.pop(index)
                except IndexError:
                    temp.pop(random.randint(0, len(temp) - 1))
                temp.insert(index, random.choice(
                    string.ascii_letters + string.digits + '! '))
                new = ''.join(temp)
            elif other == 2 and individual:
                temp = [c for c in individual]
                try:
                    temp.pop(index)
                except IndexError:
                    temp.pop(random.randint(0, len(temp) - 1))
                new = ''.join(temp)
            elif other == 3:
                temp = [c for c in individual]
                temp.insert(index, random.choice(
                    string.ascii_letters + string.digits + '! '))
                new = ''.join(temp)
            else:
                new = individual + random.choice(
                    string.ascii_letters + string.digits + '! ')

    return new


def quicksort(unsorted, low=0, high=False):
    """Quick sort the population."""
    if len(unsorted) < 2:
        return unsorted

    if high is False:
        high = len(unsorted) - 1

    if low < high:
        swapper = swap(unsorted, low, high)
        quicksort(unsorted, low, swapper - 1)
        quicksort(unsorted, swapper + 1, high)

    return unsorted


def swap(sort, low, high):
    """Swap the individuals."""
    count = low

    for index in range(low + 1, high + 1):
        if sort[index][1] <= sort[low][1]:
            count += 1
            sort[count], sort[index] = sort[index], sort[count]

    sort[count], sort[low] = sort[low], sort[count]

    return count


def main():
    """Run it."""
    count = 0
    fit = calculate_fitness_of_population(first_gen())
    if fit == 'Done!':
        return
    new_pop = breed(new_breeders(fit))
    next_gen = []
    for individual in new_pop:
        if random.randint(0, 100) < 20:
            next_gen.append(mutate(individual))
        else:
            next_gen.append(individual)
    while True:
        fit = calculate_fitness_of_population(next_gen)
        if fit == 'Done!':
            print(f'\nGenerated "Hello World!" in {count} generations')
            break
        breeders = new_breeders(fit)
        if not count % 500:
            print(f'Generation: {count} Best Guess: {breeders[0]}')
        new_pop = breed(breeders)
        next_gen = []
        for individual in new_pop:
            if random.randint(0, 100) < 5:
                next_gen.append(mutate(individual))
            else:
                next_gen.append(individual)
        count += 1
    return True


if __name__ == '__main__':
    time = timeit.timeit("main()", setup="from __main__ import main", number=1)
    print(f'It took {int(time)} seconds')
