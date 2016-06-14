import json

from juggling.utils import JugglingJSONEncoder


class JugglingNotation(object):
    def __init__(self, notation_pattern, raise_invalid=False):
        # type: (Any, int, bool)
        """
        Base class for all Juggling notations, such as :class:`SiteSwap`.

        :param notation_pattern: A juggling pattern in a format that is accepted by the notation. This will be converted
            to a :class:`Pattern` during initialization.
        :param raise_invalid: Cause the initialization of the :class:`JugglingNotation` to raise a :class:`ValueError`
            if the given pattern is deemed invalid.
        """
        # keep the provided raw pattern in case we cannot change it to a Pattern
        self.notation_pattern = notation_pattern
        # it is up to the implemented notation to create a Pattern our of the given input
        self.pattern = None

        if raise_invalid and not self.is_valid:
            raise ValueError("Pattern is not valid: '{}'".format(self.notation_pattern))

    @property
    def period(self):
        """ Property that will return the 'period', or length of beats, of the pattern before it repeats """
        return self.pattern.period

    @property
    def is_valid_syntax(self):
        """ Validates the syntax of the given pattern """
        raise ValueError("Notation has not implemented syntax validation")

    @property
    def is_valid(self):
        if self.pattern is not None:
            return self.pattern.is_valid
        return False

    def pretty_print(self):
        print(str(self.notation_pattern))

    def to_JSON(self):
        """ Return a JSON serialized version of the :class:`Notation` """
        # We build up this data dict so that we capture the @properties as well as the attributes as well as get all
        # inherited properties and values
        return json.dumps(self, sort_keys=True, indent=4, cls=JugglingJSONEncoder)
