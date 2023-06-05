import re
from abc import ABC, abstractmethod


class AbstractAction(ABC):
    """
    Abstract base class for defining actions during parsing.
    """

    def __init__(self, name):
        """
        Initializes the AbstractAction.

        Parameters:
        - name (str): The name of the action.
        """
        self.name = name

    @abstractmethod
    def __call__(self, *args):
        """
        Executes the action.

        Parameters:
        - *args: Variable number of arguments passed to the action.

        Returns:
        - The result of the action.
        """
        pass


class IdentityAction(AbstractAction):
    """
    Action that returns its first argument unchanged.
    """

    def __call__(self, *args):
        """
        Executes the action by returning the first argument.

        Parameters:
        - *args: Variable number of arguments passed to the action.

        Returns:
        - The first argument.
        """
        return args[0]


class ConcatAction(AbstractAction):
    """
    Action that concatenates its arguments into a single string.
    """

    def __call__(self, *args):
        """
        Executes the action by concatenating the arguments.

        Parameters:
        - *args: Variable number of arguments passed to the action.

        Returns:
        - The concatenated string.
        """
        result = []
        for arg in args:
            if isinstance(arg, list):
                result.append(self.__call__(*arg))
            else:
                result.append(arg)
        return "".join(result)


class IdentityListAction(AbstractAction):
    """
    Action that returns its arguments as a list.
    """

    def __call__(self, *args):
        """
        Executes the action by returning the arguments as a list.

        Parameters:
        - *args: Variable number of arguments passed to the action.

        Returns:
        - The arguments as a list.
        """
        return list(args)


class Recognizer(ABC):
    """
    Base class for creating terminal recognizers.
    """

    def __init__(self, regex):
        """
        Initializes the Recognizer.

        Parameters:
        - regex (str): Regular expression pattern used for recognition.
        """
        self.regex = re.compile(regex)

    def __call__(self, text, pos):
        """
        Performs recognition of the input text.

        Parameters:
        - text (str): The input text to recognize.
        - pos (int): The starting position in the text.

        Returns:
        - The recognized substring or None if not recognized.
        """
        match = self.regex.match(text[pos:])
        return match.group(0) if match else None
