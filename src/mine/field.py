from .tools import check_neighborhood, cords_directions
from .cell import Cell, _FAIL
from random import sample
from itertools import product
import attr

# TODO: split all of this into separate files
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
    _cells_dict = attr.ib(init=False, default={},
                          validator=attr.validators.instance_of(dict))
    _won = attr.ib(init=False, default=False,
                   validator=attr.validators.instance_of(bool))
    _loss = attr.ib(init=False, default=False,
                    validator=attr.validators.instance_of(bool))

    def __attrs_post_init__(self):
        # There is no need to calculate it over and over again
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
        self._cells_dict = {}
        for cords in cell_cords:
            self._cells_dict[cords] = Cell.make_from_tuple(cords)

    def player_check(self, cords: tuple):
        """
        Checks cell in given chords.
        """
        if (not self._cells_dict[cords].is_flagged() and
                not self._cells_dict[cords].is_revealed()):
            if self._cells_dict[cords].check() == _FAIL:
                if not self._won:
                    self._loss = True
                return _FAIL
            else:
                # after checking start revealing other
                # empty cells
                self._auto_check_cell(cords)
                self._update_won_status()
                return None

    def player_check_arround(self, cords: tuple):
        """
        Checks all cells around player choice
        """
        # check for number of flags around cell that
        # player has choosen
        n_of_flags = check_neighborhood(self._cells_dict, cords,
                                        check_func=lambda cell:
                                            cell.is_flagged())

        # cell that player choosed to check around
        check_cell = self._cells_dict[cords]

        if check_cell.is_revealed():
            for dx, dy in self._neighborhood_combinations:
                curr_cords = (cords[0]+dx, cords[1]+dy)
                try:
                    curr_cell = self._cells_dict[curr_cords]
                    if (not curr_cell.is_revealed()) and (
                            n_of_flags == check_cell.get_number()):
                        self.player_check(curr_cords)
                except KeyError:
                    pass

    # TODO: track the number of flags
    def toggle_flag(self, cords: tuple):
        """
        Toggles flag in given cords
        """
        curr_cell = self._cells_dict[cords]

        # cell has to be hidden to put flag on it
        if not curr_cell.is_revealed():
            flagged = curr_cell.is_flagged()
            self._cells_dict[cords]._flagged = not flagged
        elif curr_cell.is_revealed() and curr_cell.is_flagged():
            self._cells_dict[cords]._flagged = False
            self._cells_dict[cords].hidden = True

    def is_won(self):
        return self._won

    def is_loss(self):
        return self._loss

    def _auto_check_cell(self, cords: tuple):
        """
        Reveals all empty cells around given cords
        """
        for dx, dy in self._neighborhood_combinations:
            curr_cords = (cords[0]+dx, cords[1]+dy)
            try:
                curr_cell = self._cells_dict[curr_cords]
                if not curr_cell.is_revealed():
                    if curr_cell.is_empty():
                        # Cell is empty so we need to reveal all other
                        # cells around it
                        self._cells_dict[curr_cords].check()
                        self._auto_check_cell(curr_cords)
                    elif curr_cell.is_bomb():
                        # Cell is a bomb, so algorithm stops
                        return
                    else:
                        # Cell is a number, so algorithm reveal it
                        # and dont go deeper
                        self._cells_dict[curr_cords].check()
            except KeyError:
                continue

    def _update_won_status(self):
        """
        Checks whether game is won
        """
        hidden_bombs = 0
        other_cells = 0
        if not self._loss:
            for key in self._cells_dict:
                curr_cell = self._cells_dict[key]
                if not curr_cell.is_revealed():
                    if curr_cell.is_bomb():
                        hidden_bombs += 1
                    else:
                        other_cells += 1
            # If there are no more cells to reveal and all bombs
            # are hidden, the game is over and player won
            if (hidden_bombs - other_cells) == self.n_of_bombs:
                self._won = True

    def _fill_with_bombs(self):
        """
        Fill Field with given number of bombs
        given at initialize of object
        """
        bombs_cords = self._choose_random_bombs_cords()
        for cords in bombs_cords:
            self._cells_dict[cords]._fill_with_bomb()

    def _choose_random_bombs_cords(self):
        """
        Randomize coordinates for bombs and
        returns them
        """
        return sample(
            [*self._cells_dict], self.n_of_bombs)

    def _numberize_fields(self):
        """
        Numberize empty field based on
        coordinates of bomb fields
        """
        for cords in self._cells_dict:
            if self._cells_dict[cords].is_empty():
                n_of_bombs = check_neighborhood(self._cells_dict, cords)
                if n_of_bombs > 0:
                    self._cells_dict[cords]._numberize(n_of_bombs)
