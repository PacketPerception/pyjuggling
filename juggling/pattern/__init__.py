from collections import Iterable
from math import floor

try:
    # Python3
    from collections import UserList  # noqa
except ImportError:
    # Python2
    from UserList import UserList  # noqa

from juggling.utils import CacheProperties


__all__ = ['Pattern']


VANILLA_PATTERN = 'VSS'
MULTIPLEX_PATTERN = 'MSS'
SYNCHRONOUS_PATTERN = 'SSS'


def flatten_pattern_list(l):
    """ Flattens a pattern list into a list of tuples where each tuple is (beat, throw).

    >>> flatten_pattern_list([4,4,1])
        [(0,4),(1,4),(2,1)]
    >>> flatten_pattern_list([[53],3,1])
        [(0,5),(0,3),(1,3),(1,1)]
    >>>
    """
    # type: list -> list
    flattened = []
    for beat, el in enumerate(l):
        if isinstance(el, Iterable):
            for sub in flatten_pattern_list(el):
                flattened.append((beat, sub[1]))
        else:
            flattened.append((beat, el))
    return flattened


def convert_sss_to_mss(pattern_list):
    """ Flattens a SSS to a MSS, returns a Pattern list """
    data = []

    def mod_sync(t, mod=0):
        if isinstance(t, float):
            return floor(t) + mod
        return t

    for _ in pattern_list:
        if isinstance(_, tuple):
            d = []
            if isinstance(_[0], list):
                d.append([mod_sync(n, 1) for n in _[0]])
            else:
                d.append(mod_sync(_[0], 1))

            if isinstance(_[1], Iterable):
                d.append([mod_sync(n, -1) for n in _[1]])
            else:
                d.append(mod_sync(_[1], -1))
            data += d
        else:
            data.append(_)
    return data


def generate_state(pattern, starting_throw=0):
    # type: (Pattern, int) -> list
    """ Generates a state for a given :class:`Pattern` starting at `starting_throw` which is an
    offset into the :class:`Pattern` """

    state = [None] * (pattern.max_throw * 2)  # principal that the highest throw can go through the pattern twice
    # offset the pattern to the `starting_throw`
    starting_throw %= len(pattern.converted_to_mss)
    converted_pattern = pattern.converted_to_mss[starting_throw:] + pattern.converted_to_mss[:starting_throw]

    i = current_beat = current_prop = 0
    flattened = flatten_pattern_list(converted_pattern)
    while current_prop < pattern.num_objects:
        if flattened[i][1] == 0:
            state[current_beat] = 1
        else:
            if state[current_beat] is None:
                state[current_beat] = 1
            else:
                state[current_beat] += 1

            if state[current_beat] > 0:
                current_prop += 1

            d = current_beat + flattened[i][1]
            if state[d] is None:
                state[d] = -1
            else:
                state[d] -= 1

            i += 1
            if i == len(flattened):
                i = 0
                current_beat += 1
            elif flattened[i][0] != flattened[i-1][0]:
                current_beat += 1

    # remove trailing info
    while state and state[-1] is None or state[-1] < 0:
        del state[-1]

    if -1 in state or None in state:
        return []

    return state


class Pattern(CacheProperties, UserList):
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
        super(Pattern, self).__init__()
        UserList.__init__(self, initlist=pattern)

    def __setattr__(self, key, value):
        self._clear_cache()
        super(Pattern, self).__setattr__(key, value)

    def __setitem__(self, key, value):
        self._clear_cache()
        super(Pattern, self).__setitem__(key, value)

    @property
    def type(self):
        if isinstance(self[0], tuple):
            return SYNCHRONOUS_PATTERN

        for throw in self:
            if isinstance(throw, list):
                return MULTIPLEX_PATTERN

        return VANILLA_PATTERN

    @property
    def converted_to_mss(self):
        return convert_sss_to_mss(self.data)

    @property
    def throws_with_beats(self):
        return flatten_pattern_list(self.converted_to_mss)

    @property
    def throw_destinations(self):
        total = 0
        destination = []
        for throw in self.throws_with_beats:
            if throw[1] == 0:
                destination.append(throw[0])
            else:
                destination.append((throw[0] + throw[1]) % self.period)
                total += throw[1]
        return destination

    @property
    def incoming(self):
        incoming = [0] * self.period
        for beat, dest in enumerate(self.throw_destinations):
            if self.throws_with_beats[beat][1] != 0:
                incoming[dest] += 1
        return incoming

    @property
    def outgoing(self):
        outgoing = [0] * self.period
        for beat in range(len(self.throw_destinations)):
            if self.throws_with_beats[beat][1] != 0:
                outgoing[self.throws_with_beats[beat][0]] += 1
        return outgoing

    @property
    def is_valid(self):
        return self.incoming == self.outgoing

    def starting_with(self, throw):
        """ return the pattern if started with throw at index `throw` """
        throw %= (self.period//2) if self.type == SYNCHRONOUS_PATTERN else self.period
        return self.data[throw:] + self.data[:throw]

    @property
    def states(self):
        if self.is_valid:
            period = (self.period//2) if self.type == SYNCHRONOUS_PATTERN else self.period
            return tuple(generate_state(self, i) for i in range(0, period))
        return []

    @property
    def num_objects(self):
        def get_sum(_):
            s = 0
            for i in _:
                if isinstance(i, (tuple, list)):
                    i = get_sum(i)
                s += i
            return s
        return floor(get_sum(self.data) / self.period)

    @property
    def period(self):
        return len(self.converted_to_mss)

    @property
    def max_throw(self):
        def get_max(_, highest=0):
            for i in _:
                if isinstance(i, (tuple, list)):
                    i = get_max(i, highest)
                highest = max(i, highest)
            return highest
        return floor(get_max(self.data))  # floor in case of sync crossing throws with .5

    @property
    def ground_states(self):
        return [self.starting_with(i) for i, state in enumerate(self.states) if len(set(state)) == 1]

    @property
    def is_ground_state(self):
        if self.states:
            return len(set(self.states[0])) == 1
        return False

    @property
    def current_state(self):
        if self.states:
            return self.states[0]
        return []

    @property
    def entry_transitions(self):
        if not self.is_excited:
            return []

        transition = []
        current_throw = self.num_objects
        for beat in self.current_state:
            if beat > 0:
                transition.append(current_throw)
            else:
                current_throw += 1

        # remove any base pattern throws from the beginning
        while transition and transition[0] == self.num_objects:
            del transition[0]
        return transition

    @property
    def exit_transitions(self):
        if not self.is_excited:
            return []

        transition = []
        current_zero_loc = 0
        for i in range(0, self.num_objects):
            try:
                next_zero = self.current_state[current_zero_loc:].index(0)
                current_zero_loc = next_zero + 1
                transition.append(next_zero - i)
            except ValueError:
                transition.append(self.num_objects)

        # remove any base pattern throws from the beginning
        while transition and transition[-1] == self.num_objects:
            del transition[-1]
        return transition

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
        return len(set(self.current_state)) != 1
