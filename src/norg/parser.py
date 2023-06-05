import parglare
from parglare import GLRParser


class ParserCore:
    """
    Parser class that performs parsing using the provided grammar, terminals, and actions.
    """

    def __init__(
        self,
        grammar,
    ):
        """
        Initializes the Parser.

        Parameters:
        - grammar (str): The grammar specification in parglare format.
        """
        self.grammar = grammar

    def parse(self, string):
        """
        Parses the input string using the defined grammar, terminals, and actions.

        Parameters:
        - string (str): The input string to parse.

        Returns:
        - The parse tree.
        """

        #  TODO: (vsedov) (10:00:33 - 05/06/23): This might not be required
        #  here
        # recognizers = {
        #     terminal.name: terminal.recognizer for terminal in self.terminals
        # }
        # _actions = {action.name: action for action in self.actions}

        parser = GLRParser(
            grammar=self.grammar,
            ws="",
            debug=False,
            debug_colors=True,
        )

        try:
            trees = parser.parse(string)
        except parglare.ParseError as e:
            raise SyntaxError(e)
        assert len(trees) == 1, "Ambiguity detected - got {} parses".format(
            len(trees)
        )
        return trees
