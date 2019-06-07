import attr
from random import sample
from itertools import product

_EMPTY = '.'
_BOMB = 'x'
_FAIL = 'failed'


@attr.s
class Status:
    _label = attr.ib()

    @property
    def label(self):
        # label has to be always string
        # because it can store a numerical value
        # of bombs near cell
        return str(self._label)

    @staticmethod
    def gen_empty_status():
        """Generates empty Status object"""
        return Status(_EMPTY)

    @staticmethod
    def gen_bomb_status():
        """Generates bomb Status object"""
        return Status(_BOMB)


@attr.s
class Cell:
    """
    Stores information about single cell
    """
    x = attr.ib()
    y = attr.ib()
    status = attr.ib(validator=attr.validators.instance_of(Status))
    hidden = attr.ib(default=True,
                     validator=attr.validators.instance_of(bool))
    _flagged = attr.ib(init=False, default=False,
                       validator=attr.validators.instance_of(bool))

    def check(self):
        self.hidden = False
        if self.is_bomb():
            return _FAIL
        else:
            return None

    def is_revealed(self):
        """
        Checks whether the cell is revealed
        """
        return not self.hidden

    def get_true_label(self):
        """
        Checks label of cell, despite if it is hidden
        """
        return self.status.label

    def get_label(self):
        """
        Checks label of cell
        if it is hidden, it will return '?'
        """
        if self.hidden:
            return '?'
        elif self.flagged:
            return 'f'
        else:
            return self.status.label

    @staticmethod
    def make_from_tuple(cords: tuple):
        return Cell(cords[0], cords[1], Status.gen_empty_status())

    def _fill_with_bomb(self):
        self.status = Status.gen_bomb_status()

    def _numberize(self, number: int):
        self.status._label = number

    def is_empty(self):
        return self.status._label == _EMPTY

    def is_bomb(self):
        return self.status._label == _BOMB


@attr.s
class Field:
    """
    Field is an object which stores information
    about width, height and number of bombs in Field
    """
    width = attr.ib(default=6)
    heigth = attr.ib(default=10)
    n_of_bombs = attr.ib(default=6)


@attr.s
class MineGameField(Field):
    """
    Adds bunch of methods required to make
    a decent game from Field object
    """
    _cell_dict = attr.ib(init=False, default={},
                         validator=attr.validators.instance_of(dict))
    _won = attr.ib(init=False, default=True,
                   validator=attr.validators.instance_of(bool))
    _loose = attr.ib(init=False, default=True,
                     validator=attr.validators.instance_of(bool))

    def __attrs_post_init__(self):
        # There is no need to calculate them over and over again
        self._neighborhood_combinations = cords_directions(delete_self=True)

        self.new_game()

    def new_game(self):
        """
        Starts new game
        """
        self._generate_new_field_dict()
        self._fill_with_bombs()
        self._numberize_fields()

    def _generate_new_field_dict(self):
        """
        Generate dictionary with empty Cells, with
        coordinates based on width and heigth
        """
        cell_cords = product(
            range(self.width), range(self.heigth), repeat=1)
        for cords in cell_cords:
            self._cell_dict[cords] = Cell.make_from_tuple(cords)

    def player_check(self, cords: tuple):
        if self._cell_dict[cords].check() == _FAIL:
            self._won = False
            self._loose = True
            return _FAIL
        else:
            self._auto_check_cell(cords)

    def _auto_check_cell(self, cords: tuple):
        for dx, dy in self._neighborhood_combinations:
            curr_cords = (cords[0]+dx, cords[1]+dy)
            try:
                curr_cell = self._cell_dict[curr_cords]
                if not curr_cell.is_revealed():
                    if curr_cell.is_empty():
                        self._cell_dict[curr_cords].check()
                        self._auto_check_cell(curr_cords)
                    elif curr_cell.is_bomb():
                        return
                    else:
                        self._cell_dict[curr_cords].check()
            except KeyError:
                continue

    def _fill_with_bombs(self):
        """
        Fill Field with given number of bombs
        given at initialize of object
        """
        bombs_cords = self._choose_random_bombs_cords()
        for cords in bombs_cords:
            self._cell_dict[cords]._fill_with_bomb()

    def _choose_random_bombs_cords(self):
        """
        Randomize coordinates for bombs and
        returns them
        """
        return sample(
            [*self._cell_dict], self.n_of_bombs)

    def _numberize_fields(self):
        """
        Numberize empty field based on
        coordinates of bomb fields
        """
        for cords in self._cell_dict:
            if self._cell_dict[cords].is_empty():
                n_of_bombs = check_neighborhood(self._cell_dict, cords)
                if n_of_bombs > 0:
                    self._cell_dict[cords]._numberize(n_of_bombs)


def visualize_field(field: Field, hidden=True):
    """
    Prompts visualization of given field
    """
    for y in range(-1, field.heigth):
        for x in range(-1, field.width):
            try:
                curr_cell = field._cell_dict[(x, y)]
                if hidden:
                    to_show = f'{curr_cell.get_label()}'
                else:
                    to_show = f'{curr_cell.status._label}'
                print(to_show, end='  ')
            except KeyError:
                if x == -1 and y == -1:
                    print(" ", end=' ')
                elif x == -1:
                    print("%2d" % (y), end=' ')
                elif y == -1:
                    print("%2d" % (x), end=' ')
        print('', end='\n')


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


def check_neighborhood(cell_dict: dict, cords: tuple):
    """
    Returns number of bombs in neighborhood of cell
    in given dictionary.
    """
    neighborhood_combinations = cords_directions()

    n_of_bombs = 0
    for dx, dy in neighborhood_combinations:
        try:
            x = cords[0]
            y = cords[1]
            current_cell = cell_dict[(x+dx, y+dy)]
            if current_cell.is_bomb():
                n_of_bombs += 1
        except KeyError:
            pass
    return n_of_bombs


if __name__ == '__main__':
    test_field = MineGameField(8, 8, n_of_bombs=4)
    visualize_field(test_field, hidden=False)
    print(3*'-\n')
    visualize_field(test_field)
    print(3*'-\n')
    while True:
        x = input("Enter x: ")
        y = input("Enter y: ")
        cords = (int(x), int(y))
        test_field.player_check(cords)
        print(3*'-\n')
        visualize_field(test_field)
