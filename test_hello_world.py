"""Tests for hello_world.py."""

import hello_world as h


def test_perfect_fitness():
    assert h.fitness('Hello World!') == 'Done!'


def test_not_fitness_match():
    assert h.fitness('Hello World') == 10


def test_first_gen_length():
    test = h.first_gen()
    assert len(test) == 100


def test_first_gen_randomness():
    test = h.first_gen()
    for i in range(99):
        assert test[i] != test[i + 1]


def test_fitness_calculation_length():
    test_pop = h.first_gen()
    test = h.calculate_fitness_of_population(test_pop)
    assert len(test) == 100


def test_fitness_calculation_changes_format():
    test_pop = h.first_gen()
    test = h.calculate_fitness_of_population(test_pop)
    for i in test:
        assert len(i) == 2


def test_fitness_calculation_is_accurate():
    test_pop = h.first_gen()
    test = h.calculate_fitness_of_population(test_pop)
    for i in test:
        assert i[1] == h.fitness(i[0])


def test_parent_length():
    test_pop = h.calculate_fitness_of_population(h.first_gen())
    test = h.new_breeders(test_pop)
    assert len(test) == 50


def test_parents_are_good():
    test_pop = h.calculate_fitness_of_population(h.first_gen())
    test = h.new_breeders(test_pop)
    for i in range(24):
        assert h.fitness(test[i][0]) >= h.fitness(test[i + 1][0])


def test_breed_length():
    test_pop = h.new_breeders(h.calculate_fitness_of_population(h.first_gen()))
    test = h.breed(test_pop)
    assert len(test) == 100


def test_proper_breeding():
    test_pop = h.new_breeders(h.calculate_fitness_of_population(h.first_gen()))[:2]
    parent1, parent2 = test_pop
    test = h.breed(test_pop)
    for child in test:
        for i in range(len(child)):
            assert child[i] == parent1[0][i] or child[i] == parent2[0][i]


def test_basic_quicksort():
    unsorted = [['a', 2], ['a', 1]]
    assert h.quicksort(unsorted) == [['a', 1], ['a', 2]]


def test_one_element():
    unsorted = [['a', 1]]
    assert h.quicksort(unsorted) == [['a', 1]]


def test_less_basic_quicksort():
    unsorted = [['a', 2], ['a', 4], ['a', 3], ['a', 1]]
    assert h.quicksort(unsorted) == [['a', 1], ['a', 2], ['a', 3], ['a', 4]]


def test_reversed_quicksort():
    unsorted = [['a', 10], ['a', 9], ['a', 8], ['a', 7], ['a', 6], ['a', 5], ['a', 4], ['a', 3], ['a', 2], ['a', 1]]
    assert h.quicksort(unsorted) == [['a', 1], ['a', 2], ['a', 3], ['a', 4], ['a', 5], ['a', 6], ['a', 7], ['a', 8], ['a', 9], ['a', 10]]


def test_complex_quicksort():
    unsorted = [['a', 49], ['a', 682], ['a', -9000], ['a', 62], ['a', 8473], ['a', -47], ['a', 1]]
    assert h.quicksort(unsorted) == [['a', -9000], ['a', -47], ['a', 1], ['a', 49], ['a', 62], ['a', 682], ['a', 8473]]


def test_mutate_changes():
    test_pop = h.first_gen()
    for individual in test_pop:
        new = h.mutate(individual)
        assert new != individual


def test_mutate_length():
    test_pop = h.first_gen()
    for individual in test_pop:
        new = h.mutate(individual)
        assert len(new) - 1 == len(individual) or len(new) + 1 == len(individual) or len(new) == len(individual)


def test_main():
    assert h.main() == True
