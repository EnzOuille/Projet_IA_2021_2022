import random
import copy
from sudoku_enzo import solve_sudoku, print_grid

NB_VAR=60

def population_initialization():
    first_population = []
    for population_size in range(5):
        grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        for i in range(NB_VAR):
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            while grid[x][y] != 0:
                x = random.randint(0, 8)
                y = random.randint(0, 8)
            grid[x][y] = random.randint(1, 9)
        first_population.append(grid)
    return first_population


def grid_evaluation(arr):
    evaluation_result = 0
    for line in range(9):
        for column in range(9):
            if arr[line][column] != 0:
                evaluation_result += check_case(arr, line, column)
    return evaluation_result


def check_case(arr, line, column):
    case_value = arr[line][column]
    nb_appearance_in_column = 0
    for x in range(9):
        if arr[x][column] == case_value:
            nb_appearance_in_column += 1

    if arr[line].count(case_value) > 1 or nb_appearance_in_column > 1:
        return 0
    return 1


def evolution(grid_one, grid_two):
    # print("---------------------------")
    # print(grid_evaluation(grid_one))
    # print(grid_evaluation(grid_two))
    # print("---------------------------\n")
    new_population = []
    for i in range(5):
        random_stat = random.random()
        if random_stat <= 0.5:
            new_population.append(random.choice([grid_one, grid_two]))
        elif random_stat <= 0.7:
            new_population.append(mutate(random.choice([grid_one, grid_two])))
        else:
            new_population.append(crossover(grid_one, grid_two))
    return new_population


def crossover(grid_one, grid_two):
    new_grid = []
    for line in range(9):
        new_grid.append([])
        for column in range(9):
            if grid_one[line][column] != grid_two[line][column]:
                new_grid[line].append(random.choice([grid_one[line][column], grid_two[line][column]]))
            else:
                new_grid[line].append(grid_one[line][column])
    return new_grid


def mutate(arr):
    new_grid = arr.copy()
    new_grid[random.randint(0, 8)][random.randint(0, 8)] = random.randint(1, 9)
    return new_grid


def population_evolution(population):
    grid_one = [[], -1]
    grid_two = [[], -1]
    for grid in population:
        evaluation_value = grid_evaluation(grid)
        if evaluation_value > grid_two[1]:
            if evaluation_value > grid_one[1]:
                grid_two = grid_one
                grid_one = [grid, evaluation_value]
            else:
                grid_two = [grid, evaluation_value]
    return evolution(grid_one[0], grid_two[0])


def main():
    population = population_initialization()
    print_population(population)
    nb_iteratation=0
    resolu=False
    copy_grid=[]
    while not resolu:
        population = population_evolution(population)
        """
        calcul du meilleur element
        """
        max=(grid_evaluation(population[0]))
        index=0
        for child in population:
            if max<grid_evaluation(child):
                max=grid_evaluation(child)
                index=population.index(child)
        if max >= NB_VAR:
            copy_grid=copy.deepcopy(population[index])
            resolu=solve_sudoku(copy.deepcopy(population[index]))
            print(resolu)
        nb_iteratation+=1
    print("Grille généré : \n")
    print_grid(copy_grid)

def print_population(population):
    for grid in population:
        print_grid(grid)
        print(grid_evaluation(grid))
        print("\n")


def print_grid(arr):
    for line in arr:
        print(line)


main()
