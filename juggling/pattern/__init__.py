from math import floor

try:
    # Python3
    from collections import UserList  # noqa
except ImportError:
    # Python2
    from UserList import UserList  # noqa


__all__ = ['Pattern']


class Pattern(UserList):
    """
    The base representation of any juggling pattern, regardless of notation. A :class:`Pattern` looks
    and acts like a list, but has some specific constraints about how data can be stored in it.

    >>> p = Pattern([4, 4, 1])
    >>> p.is_symmetric == True
    >>> p.period == 3
    >>> p.is_excited == False

    """
    def __init__(self, pattern):
        # TODO: this is a stop-gap, follow the discussion on the group to figure out how we're actually
        super(Pattern, self).__init__(initlist=pattern)

        # TODO: implement state generation
        self.states = []

    @property
    def num_objects(self):
        # TODO: make this handle everything
        return floor(sum(self.data) / self.period)

    @property
    def period(self):
        # TODO: implement
        return len(self.data)

    @property
    def ground_state(self):
        # TODO: implement
        return None

    @property
    def current_state(self):
        # TODO: implement
        return None

    @property
    def transistions(self):
        # TODO: implement
        return None

    @property
    def is_symmetric(self):
        """ Returns True if this pattern is symmetric, the pattern repeats with the opposite hand """
        return bool(self.period & 0x1)

    @property
    def is_asymmetric(self):
        """ Returns True if this pattern is asymmetric, the pattern repeats with the same hand """
        return not self.is_symmetric

    @property
    def is_excited(self):
        # TODO: implement
        return False
