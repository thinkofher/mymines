from random import randint
from itertools import product

EMPTY = 'o'
BOMB = 'x'
NUMBER = int


def gen_field_matrix(width=8, heigth=10):
    ans_matrix = []
    for _ in range(heigth):
        ans_matrix.append([EMPTY] * width)
    return ans_matrix


# TODO: Search for some itertools implementation
def add_random_bomb_cords(cords_list, width, heigth):

    # Substract 1 because of list indexing starts at 0
    bomb_cords = (randint(0, width-1),
                  randint(0, heigth-1))
    if bomb_cords in cords_list:
        add_random_bomb_cords(cords_list, width, heigth)
    else:
        cords_list.append(bomb_cords)


# TODO: make it more elegant, and create two functions instead
#       of one big
def fill_with_bombs(matrix, n_of_bombs=5):
    width, heigth = len(matrix[0]), len(matrix)
    random_bombs_cords = []
    for _ in range(n_of_bombs):
        add_random_bomb_cords(random_bombs_cords, width, heigth)
    for cords in random_bombs_cords:
        width, heigth = cords
        matrix[heigth][width] = BOMB
    return matrix


def check_neighborhood(matrix, x, y):
    """
    Returns number of bombs in neighborhood of cell
    """
    # Create all possible combinations of neighboor location
    # Example: (-1, 1), (0, 1), (1, 0) ...
    neighborhood_combinations = list(product([-1, 0, 1], repeat=2))

    # Remove coordinates of the cell subjected to analysis
    neighborhood_combinations.remove((0, 0))

    n_of_bombs = 0
    for dx, dy in neighborhood_combinations:
        try:
            current_cell = matrix[y+dy][x+dx]
            if current_cell == BOMB:
                n_of_bombs += 1
        except IndexError:
            pass
    return n_of_bombs


def numbering_field(matrix):
    for y, width_vector in enumerate(matrix):
        for x, cell in enumerate(width_vector):
            if cell != BOMB:
                n_of_bombs = check_neighborhood(matrix, x, y)
                matrix[y][x] = n_of_bombs
    return matrix


def visualize_field(matrix):
    for width_vector in matrix:
        width_vector = [str(elem) for elem in width_vector]
        print(' '.join(width_vector))


if __name__ == '__main__':
    field = gen_field_matrix()
    field = fill_with_bombs(field, 6)
    field = numbering_field(field)
    visualize_field(field)
