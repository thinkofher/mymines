from itertools import product


def cords_directions(delete_self=True):
    """
    Returns list with combinations of directions
    for searching in neighborhood
    """
    # Create all possible combinations of neighboor location
    # Example: (-1, 1), (0, 1), (1, 0) ...
    neighborhood_combinations = list(product([-1, 0, 1], repeat=2))

    if delete_self:
        # Remove coordinates of the cell subjected to analysis
        neighborhood_combinations.remove((0, 0))

    return neighborhood_combinations


def check_neighborhood(cell_dict: dict, cords: tuple,
                       check_func=lambda cell: cell.is_bomb(),
                       check_self=False):
    """
    Returns number of bombs in neighborhood of cell
    in given dictionary.
    """
    neighborhood_combinations = cords_directions(not check_self)

    n_of_things = 0
    for dx, dy in neighborhood_combinations:
        try:
            x = cords[0]
            y = cords[1]
            current_cell = cell_dict[(x+dx, y+dy)]
            if check_func(current_cell):
                n_of_things += 1
        except KeyError:
            pass
    return n_of_things


def visualize_field(field, hidden=True):
    """
    Prompts visualization of given field
    """
    for y in range(-1, field.heigth):
        for x in range(-1, field.width):
            try:
                curr_cell = field._cells_dict[(x, y)]
                if hidden:
                    to_show = f'[{curr_cell.get_label()}]'
                else:
                    to_show = f'[{curr_cell.get_true_label()}]'
                print(to_show, end='  ')
            except KeyError:
                if x == -1 and y == -1:
                    print(" ", end=' ')
                elif x == -1:
                    print("%3d" % (y), end=' ')
                elif y == -1:
                    print("%4d" % (x), end=' ')
        print('', end='\n')
