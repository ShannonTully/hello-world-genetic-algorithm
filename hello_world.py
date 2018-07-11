"""This program will print 'Hello World!' using a genetic algorithm."""

import random  # used for random number and string generation
import timeit  # used to track how long the program took to run
import string  # used for string charactors
import sys     # used for command line arguments


def fitness(guess, message):
    """
    Determine the fitness score of an individual.

    This takes in two strings to compare and returns the score (or fitness)
    for the closeness of the first string to the second one.
    """
    if guess == message:  # if the message is found
        return 'Done!'

    i = 0
    if len(message) < len(guess):  # iterate through shorter string
        score = 0
        for i in range(len(message)):
            # if letter in guess and message are the same
            if guess[i] == message[i]:
                score += 1
    else:
        score = 0
        for i in range(len(guess)):
            if guess[i] == message[i]:
                score += 1
    # calculate score using matching letters and lengths
    return score - abs(len(guess) - len(message))


def first_gen():
    """
    Generate the first population.

    This takes no arguments and returns a list of 100 random strings
    with lengths between 1 and 100.
    """
    i = 0
    population = []

    for i in range(100):
        population.append(
            ''.join(
                random.choice(
                    string.ascii_letters + string.digits + '! '
                ) for _ in range(random.randint(1, 100))))

    return population


def calculate_fitness_of_population(population, message):
    """
    Take in a population and return them with their scores.

    This takes in a list of strings and calculates the fitness of each
    string returning a list of sublists where the first value of each
    sublist is the original string and the second value is its score.
    """
    pop_with_fitness = []

    for individual in population:
        fit = fitness(individual, message)
        if fit == 'Done!':
            return fit
        pop_with_fitness.append([individual, fit])

    return pop_with_fitness  # [[string, integer], [string, integer]...]


def new_breeders(pop_with_fitness):
    """
    Take in pop with fitness and return breeding population.

    This takes in a population that has its fitness calculated from
    the function calculate_fitness_of_population and finds the top 25
    scores and 25 extra from the lower 75 scores.

    This also returns the worst individual in the population as the second
    item in an array.
    """
    sorted_pop = sort(pop_with_fitness)
    worst = sorted_pop[0]  # used for UI
    breeders = []
    # used for getting good things in the bottom 75
    weights = [int((2 / x) * 100) for x in range(1, 51)]

    i = 0
    for i in range(99, 74, -1):  # get the top 25
        breeders.append(sorted_pop[i])

    extras = [random.choices(sorted_pop[-50:], weights)[0] for _ in range(25)]

    breeders.extend(extras)
    return [breeders, worst]


def breed(breeders):
    """
    Take in breeders and return new pop.

    Input should be a list of 50 lists containing strings and their
    scores.

    This takes two items at random for breeding and creates 4 children
    from this pairing and selects more two at a time until there are
    none left.

    Returns 100 strings in a list.
    """
    new_pop = []

    i = 0
    for i in range(50):
        if len(breeders) > 1:
            parents = [0, 0]  # initialize parents
            child = ['', '', '', '']   # initialize children
            parents[0] = random.choice(breeders)  # random parent
            breeders.remove(parents[0])
            parents[1] = random.choice(breeders)  # random parent
            breeders.remove(parents[1])

            if len(parents[0][0]) > len(parents[1][0]):  # longest parent last
                parents[0], parents[1] = parents[1], parents[0]

            for k in range(4):  # for each child
                if random.randint(0, 100) < 50:  # pick a parent's length
                    length = parents[0][0]
                else:
                    length = parents[1][0]

                # child will be the length of chosen parent
                for j in range(len(length)):
                    number = random.randint(0, 100)
                    if (number < 50) and (j < len(parents[0][0])):
                        child[k] += str(parents[0][0][j])
                    else:
                        child[k] += str(parents[1][0][j])

            for k in range(4):  # add new children to population
                if child[k]:
                    new_pop.append(child[k])
                else:
                    new_pop.append('!')

    return new_pop


def mutate(individual):
    """
    Take in a string and change it.

    Possible mutations are:
    Change a random letter,
    Remove a random letter,
    Insert a random letter in a random location,
    Add either one or two random letters to the end.
    """
    new = individual
    chars = string.ascii_letters + string.digits + '! '
    while new == individual:
        other = random.randint(1, 4)
        if other == 1:  # Change a random letter
            temp = [c for c in individual]
            place = random.randint(0, len(temp) - 1)
            temp.pop(place)
            temp.insert(place, random.choice(chars))
            new = ''.join(temp)
        elif other == 2 and individual:  # Remove a random letter
            temp = [c for c in individual]
            temp.pop(random.randint(0, len(temp) - 1))
            if temp:
                new = ''.join(temp)
            else:
                new = individual
        elif other == 3:  # Insert a random letter in a random location
            temp = [c for c in individual]
            temp.insert(random.randint(0, len(temp) - 1), random.choice(chars))
            new = ''.join(temp)
        else:  # Add either one or two random letters to the end
            if random.randint(0, 100) > 50:
                new = individual + random.choice(chars)
            else:
                new = individual + random.choice(
                    chars) + random.choice(
                        chars)

    return new


def sort(unsorted, low=0, high=False):
    """Sort the population worst score to best."""
    def swap(sort, low, high):
        """Sort helper."""
        count = low

        for index in range(low + 1, high + 1):
            if sort[index][1] <= sort[low][1]:
                count += 1
                sort[count], sort[index] = sort[index], sort[count]

        sort[count], sort[low] = sort[low], sort[count]

        return count

    if len(unsorted) < 2:
        return unsorted

    if high is False:
        high = len(unsorted) - 1

    if low < high:
        swapper = swap(unsorted, low, high)
        sort(unsorted, low, swapper - 1)
        sort(unsorted, swapper + 1, high)

    return unsorted


def main(message, number=45):
    """Run program."""
    count = 1  # tracks generation number
    mod = 200

    if len(message) > 99:
        print('Please make your message less than 100 charactors')
        return False

    for char in message:
        if char not in (string.ascii_letters + string.digits + '! '):
            print(
                'Letters, Numbers, Spaces, and Exclamation points only please.'
            )
            return False

    # [[string, integer], [string, integer]...]
    fit = calculate_fitness_of_population(first_gen(), message)

    if fit == 'Done!':
        print(f'Generated "{message}" in the first generation')
        return True

    breeders, worst = new_breeders(fit)  # parents for next population
    print(f'Generation:  First\n')
    print(f'Best Guess:  {breeders[0]}\nWorst Guess: {worst}\n')
    new_pop = breed(breeders)  # 100 new individuals
    next_gen = []

    for individual in new_pop:  # % chance to mutate individual
        if random.randint(0, 100) < number:
            next_gen.append(mutate(individual))
        else:
            next_gen.append(individual)

    while True:
        # [[string, integer], [string, integer]...]
        fit = calculate_fitness_of_population(next_gen, message)

        if fit == 'Done!':
            print(f'Generated "{message}" in {count} generations')
            break

        breeders, worst = new_breeders(fit)  # parents for next population

        # this is to make sure your terminal doesn't get spammed
        if not count % mod:
            print(f'Generation:  {count}\n')
            print(f'Best Guess:  {breeders[0]}\nWorst Guess: {worst}\n')
            if count == 1600:
                print('Almost Done!\n')
            elif count == 3200:
                print('Final Few!\n')
            elif count == 6400:
                print('This is taking a while...\n')
            elif count == 12800:
                print('What have you done to me.\n')
            mod *= 2

        new_pop = breed(breeders)  # 100 new individuals
        next_gen = []

        for individual in new_pop:  # % chance to mutate individual
            if random.randint(0, 100) < number:
                next_gen.append(mutate(individual))
            else:
                next_gen.append(individual)

        count += 1

    return count


def get_message():
    """Get the inputted message."""
    message = ''
    message = ' '.join(sys.argv[1:])

    if message:
        return message
    else:
        return 'Hello World!'  # default message


if __name__ == '__main__':
    time = timeit.timeit(
        f'main({repr(get_message())})',
        setup="from __main__ import main",
        number=1
    )
    print(f'It took {int(time)} seconds')
