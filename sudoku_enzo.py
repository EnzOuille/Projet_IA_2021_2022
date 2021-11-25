import copy
import time


def print_grid(arr):
    for i in range(9):
        for j in range(9):
            print(arr[i][j], end=" ")
        print()


def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if (arr[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False


def used_in_row(arr, row, num):
    for i in range(9):
        if num != 0:
            if (arr[row][i] == num and num != 0):
                return True
    return False


def used_in_col(arr, col, num):
    for i in range(9):
        if (num != 0):
            if (arr[i][col] == num):
                return True
    return False


def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if (num != 0):
                if (arr[i + row][j + col] == num):
                    return True
    return False


def check_location_is_safe(arr, row, col, num):
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % 3,
                                                                                                 col - col % 3, num)


results = []


def verif_grid(arr):
    for i in range(9):
        for j in range(9):
            if verif_grid_constraint(arr, i, j, arr[i][j]):
                return False
    return True


def verif_grid_constraint(arr, row, col, num):
    for i in range(9):
        if num != 0 and i != col:
            if arr[row][i] == num:
                return True
    for i in range(9):
        if num != 0 and i != row:
            if arr[i][col] == num:
                return True
    row2 = row - row % 3
    col2 = col - col % 3
    for i in range(3):
        for j in range(3):
            if num != 0 and (i+row2 != row or j+col2 != col):
                if arr[i + row2][j + col2] == num:
                    return True
    return False


def solve_sudoku(arr):
    l = [0, 0]
    if (not find_empty_location(arr, l)):
        return True
    row = l[0]
    col = l[1]
    for num in range(1, 10):
        if (check_location_is_safe(arr,
                                   row, col, num)):
            arr[row][col] = num
            if (solve_sudoku(arr)):
                return True
            arr[row][col] = 0
    return False


def brute_force(arr):
    print("Starting BruteForce")
    count = 0
    lines = 0
    for line in arr:
        for x in range(9):
            if line[x] == 0:
                for y in range(1, 10):
                    temp_array = copy.deepcopy(arr)
                    if (check_location_is_safe(temp_array, lines, x, y)):
                        temp_array[lines][x] = y
                        if (solve_sudoku(temp_array)):
                            if not temp_array in results:
                                results.append(temp_array)
                                count += 1
        lines += 1
    return count


if __name__ == "__main__":
    # creating a 2D array for the grid
    # assigning values to the grid
    # grid = [[1, 6, 2, 8, 5, 7, 4, 9, 3],
    #         [5, 3, 4, 1, 2, 9, 6, 7, 8],
    #         [7, 8, 9, 6, 4, 3, 5, 2, 1],
    #         [4, 7, 5, 3, 1, 2, 9, 8, 6],
    #         [9, 1, 3, 5, 8, 6, 7, 4, 2],
    #         [6, 2, 8, 7, 9, 4, 1, 3, 5],
    #         [3, 5, 6, 4, 7, 8, 2, 1, 9],
    #         [2, 4, 1, 9, 3, 5, 8, 6, 7],
    #         [8, 9, 7, 2, 6, 1, 3, 5, 0]]

    # assigning values to the grid
    # grid = [[2, 0, 0, 0, 6, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 1, 3, 6],
    #         [0, 4, 0, 9, 0, 0, 2, 0, 0],
    #         [0, 0, 0, 0, 7, 2, 0, 0, 0],
    #         [0, 7, 0, 0, 0, 0, 0, 4, 0],
    #         [0, 0, 0, 5, 1, 0, 0, 0, 0],
    #         [0, 0, 2, 0, 0, 8, 0, 9, 0],
    #         [1, 5, 7, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 3, 0, 0, 0, 7]]

    grid = [[2, 9, 5, 7, 4, 3, 8, 6, 1],
            [4, 3, 1, 8, 6, 5, 9, 0, 0],
            [8, 7, 6, 1, 9, 2, 5, 4, 3],
            [3, 8, 7, 4, 5, 9, 2, 1, 6],
            [6, 1, 2, 3, 8, 7, 0, 9, 5],
            [5, 4, 9, 2, 1, 6, 7, 3, 8],
            [7, 6, 3, 5, 0, 4, 1, 8, 9],
            [9, 2, 8, 6, 7, 1, 3, 5, 4],
            [1, 5, 4, 9, 3, 8, 0, 0, 0]]

    results = []
    copy_grid = copy.deepcopy(grid)
    solutions = brute_force(grid)
    if verif_grid(copy_grid):
        start = time.time()
        if (solve_sudoku(copy_grid)):
            end = time.time()
            print_grid(grid)
            print("---")
            print_grid(copy_grid)
            print("Il y a : " + str(solutions) + " solutions.")
            print("La résolution de la grille a pris {:.3f}".format(end - start) + " secondes.")
        else:
            print("No solution exists")
    else:
        print("La grille de base n'est pas valide")
