from parglare import Grammar

from src.norg.abstract.actions import ConcatAction, IdentityAction


class GrammarGenerator:
    def __init__(self, document_structure, terminal_patterns):
        self.document_structure = document_structure
        self.terminal_patterns = terminal_patterns

    def generate_grammar(self):
        """Generate a parglare grammar from the document structure and terminal patterns.

        Returns
        -------
        Grammar String of current structure based on document_structure.py
            String representation of the grammar.
        """
        doc_names = " | ".join(
            [action.name for action in self.document_structure]
        )
        grammar = f"document: ({doc_names})*;\n\n"

        for action in self.document_structure:
            if isinstance(action, ConcatAction):
                grammar += f"{action.name}: {' '.join(action.elements)};\n"
            elif isinstance(action, IdentityAction):
                grammar += f"{action.name}: {action.name.lower()};\n"

        grammar += "\n"
        grammar += "terminals\n"

        for terminal, pattern in self.terminal_patterns.items():
            grammar += f"{terminal}: /{pattern}/;\n"

        print(grammar)
        print(
            "──────────────────────────────────────────────────────────────────────"
        )
        return grammar

    def parser(self, file=False):
        """Generate a parglare parser from the document structure and terminal patterns.

        Returns
        -------
        GLRParser
            Parser object.
        """
        return {
            True: Grammar.from_file,
            False: Grammar.from_string,
        }[
            file
        ]("norg.pg" if file else self.generate_grammar())

    def save_to_file(self, file_name):
        """
        Save the grammar to a file.
        """
        with open(f"{file_name}.pg", "w") as f:
            f.write(self.generate_grammar())
