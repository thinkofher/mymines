import attr
from random import sample
from itertools import product

_EMPTY = ''
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

    def check(self):
        if self.is_bomb():
            return _FAIL
        else:
            self.hidden = False
            return None

    @staticmethod
    def make_from_tuple(cords):
        return Cell(cords[0], cords[1], Status.gen_empty_status())

    def _fill_with_bomb(self):
        self.status = Status.gen_bomb_status()

    def _numberize(self, number):
        self.status._label = number

    def is_empty(self):
        if self.status._label != _BOMB:
            return True
        else:
            return False

    def is_bomb(self):
        if self.status._label == _BOMB:
            return True
        else:
            return False


@attr.s
class Field:
    """
    Field is an object which stores information
    about cells and has methods to fill them with
    bombs and numberize.
    """
    width = attr.ib(default=6)
    heigth = attr.ib(default=10)
    n_of_bombs = attr.ib(default=6)
    _cell_dict = attr.ib(init=False, default={},
                         validator=attr.validators.instance_of(dict))

    def __attrs_post_init__(self):
        self.generate_new_field_dict()
        self._fill_with_bombs()
        self._numberize_fields()

    def generate_new_field_dict(self):
        """
        Generate dictionary with empty Cells, with
        coordinates based on width and heigth
        """
        cell_cords = product(
            range(self.width), range(self.heigth), repeat=1)
        for cords in cell_cords:
            self._cell_dict[cords] = Cell.make_from_tuple(cords)

        # as soon as we have dictionary with cells
        # we can fill field with bombs and numberize cells
        self._fill_with_bombs()
        self._numberize_fields()

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
                self._cell_dict[cords]._numberize(n_of_bombs)


def visualize_field(field):
    for y in range(field.heigth):
        for x in range(field.width):
            curr_cell = field._cell_dict[(x, y)]
            print(f'{curr_cell.status.label}', end=' ')
        print('', end='\n')


def check_neighborhood(cell_dict, cords):
    """
    Returns number of bombs in neighborhood of cell
    in give dictionary.
    """
    # Create all possible combinations of neighboor location
    # Example: (-1, 1), (0, 1), (1, 0) ...
    neighborhood_combinations = list(product([-1, 0, 1], repeat=2))

    # Remove coordinates of the cell subjected to analysis
    neighborhood_combinations.remove((0, 0))

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
    test_field = Field(10, 20)
    visualize_field(test_field)
