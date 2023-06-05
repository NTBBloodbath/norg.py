import parglare
from attr import attrib, attrs
from parglare import GLRParser, Grammar

from src.norg.abstract.actions import ConcatAction, IdentityAction, Terminal


class ParserCore:
    """
    Parser class that performs parsing using the provided grammar, terminals, and actions.
    """

    def __init__(self, grammar, terminals, actions):
        """
        Initializes the Parser.

        Parameters:
        - grammar (str): The grammar specification in parglare format.
        - terminals (list): List of Terminal objects representing the terminal symbols.
        - actions (list): List of AbstractAction objects representing the parsing actions.
        """
        self.grammar = grammar
        self.terminals = terminals
        self.actions = actions

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
            print(trees)
        except parglare.ParseError as e:
            raise SyntaxError(e)
        assert len(trees) == 1, "Ambiguity detected - got {} parses".format(
            len(trees)
        )
        return trees


example_norg_format = """
* Heading 1
    Item work content inside
    ** Heading 2
        Item work content inside
        @code Block
        This is some eaxmple code
        @end
""".strip()

grammar = r"""
document: (Heading| LIST| AT | TEXT)*;

Heading: heading text;
LIST: list text;
AT: at_block text at_end;
TEXT: text;

terminals
heading: /\*+/;
list: /\-+/;
at_block: /@[\w]+/;
at_end: /@end/;
text : /[^@\*\-]+/;
"""


document_structure = [
    ConcatAction("Heading", ["heading", "text"]),
    ConcatAction("LIST", ["list", "text"]),
    ConcatAction("AT", ["at_block", "text", "at_end"]),
    IdentityAction("TEXT", ["text"]),
]

terminal_patterns = {
    "heading": r"\*+",
    "list": r"\-+",
    "at_block": r"@[\w]+",
    "at_end": r"@end",
    "text": r"[^@\*\-]+",
}

terminals = {
    name: Terminal(pattern) for name, pattern in terminal_patterns.items()
}


def generate_grammar(document_structure, terminal_patterns):
    doc_names = " | ".join([action.name for action in document_structure])
    grammar = f"document: ({doc_names})*;\n\n"

    for action in document_structure:
        if isinstance(action, ConcatAction):
            grammar += f"{action.name}: {' '.join(action.elements)};\n"
        elif isinstance(action, IdentityAction):
            grammar += f"{action.name}: {action.name.lower()};\n"

    grammar += "\n"
    grammar += "terminals\n"

    for terminal, pattern in terminal_patterns.items():
        grammar += f"{terminal}: /{pattern}/;\n"

    return grammar


print(generate_grammar(document_structure, terminal_patterns))
parser = ParserCore(
    generate_grammar(document_structure, terminal_patterns),
    terminals,
    document_structure,
)
print(parser.parse(example_norg_format))
