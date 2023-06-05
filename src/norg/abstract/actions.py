import re
from abc import ABC, abstractmethod
from typing import Optional

import attr


@attr.s(auto_attribs=True)
class Action(ABC):
    """
    Abstract base class for grammar actions.

    Attributes
    ----------
    None

    Methods
    -------
    process(self, *args):
        Abstract method to be implemented by subclasses. Processes the given arguments and returns the result.
    """

    @abstractmethod
    def process(self, *args):
        pass


@attr.s(auto_attribs=True)
class IdentityAction(Action):
    """
    Class for an identity action in the grammar.

    Attributes
    ----------
    name : str
        The name of the identity action.
    elements : Optional[list]
        A list of elements associated with the identity action.

    Methods
    -------
    process(self, *args):
        Processes the given arguments and returns the result. In the case of an IdentityAction, it returns the first argument.
    """

    name: str
    elements: Optional[list]

    def process(self, *args):
        return args[0]


@attr.s(auto_attribs=True)
class ConcatAction(Action):
    """
    Class for a concatenation action in the grammar.

    Attributes
    ----------
    name : str
        The name of the concatenation action.
    elements : list
        A list of elements to be concatenated.

    Methods
    -------
    process(self, *args):
        Processes the arguments and concatenates them, returning a formatted string with the name and the concatenated elements.
    """

    name: str
    elements: list

    def process(self, *args):
        result = []
        for arg in args:
            if isinstance(arg, list):
                result.append(self.process(*arg))
            else:
                result.append(arg)
        return f'{self.name}: {" ".join(result)}'


@attr.s(auto_attribs=True)
class Terminal:
    """
    Class for a terminal in the grammar.

    Attributes
    ----------
    pattern : str
        The terminal pattern as a regular expression.

    Methods
    -------
    match(self, text: str, pos: int) -> Optional[str]:
        Tries to match the terminal pattern in the given text at the specified position.
        If matched, returns the matched string; otherwise, returns None.
    """

    pattern: str = attr.ib(converter=re.compile)

    def match(self, text: str, pos: int) -> Optional[str]:
        """
        Tries to match the terminal pattern in the given text at the specified position.

        Parameters
        ----------
        text : str
            The text to search for a matching terminal pattern.
        pos : int
            The position in the text where the search should start.

        Returns
        -------
        Optional[str]
            The matched string if the terminal pattern is found, or None otherwise.
        """
        match = self.pattern.match(text[pos:])
        return match.group(0) if match else None
