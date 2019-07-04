import attr

EMPTY = '.'
BOMB = 'x'
FLAGGED = 'f'
HIDDEN = '?'
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
        return Status(EMPTY)

    @staticmethod
    def gen_bomb_status():
        """Generates bomb Status object"""
        return Status(BOMB)


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
        """
        When playing, player is checking
        if there is a bomb hidden in cell
        or not.
        """
        self.hidden = False
        if self.is_bomb():
            return _FAIL
        else:
            return None

    def is_flagged(self):
        """
        Checks whether the cell is flagged
        """
        return self._flagged

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
        if self._flagged:
            return FLAGGED
        elif self.hidden:
            return HIDDEN
        else:
            return self.status.label

    def get_number(self):
        """
        Returns the number given to that Cell
        during the game
        """
        try:
            number = int(self.status.label)
            return number
        except ValueError:
            # There is no number given to this Cell
            return None

    def is_empty(self):
        return self.status._label == EMPTY

    def is_bomb(self):
        return self.status._label == BOMB

    @staticmethod
    def make_from_tuple(cords: tuple):
        """
        Returns empty cell with given coordinates
        """
        return Cell(cords[0], cords[1], Status.gen_empty_status())

    def _fill_with_bomb(self):
        self.status = Status.gen_bomb_status()

    def _numberize(self, number: int):
        self.status._label = number
