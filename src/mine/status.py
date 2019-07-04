import attr
from .cell import EMPTY, BOMB


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
