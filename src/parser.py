from ply import yacc

from src.lexer import NorgLexer


class NorgParser(NorgLexer):
    def __init__(self):
        super().__init__()
        self.parser = yacc.yacc(module=self)

    # Parser rules

    def p_document(self, p):
        """document : block
        | block document"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_block(self, p):
        """block : heading
        | listitem
        | text
        | task
        | label"""
        p[0] = p[1]

    def p_heading(self, p):
        "heading : HEADING"
        p[0] = {"type": "heading", "level": len(p[1][0]), "content": p[1][1]}

    def p_listitem(self, p):
        "listitem : LISTITEM"
        p[0] = {"type": "listitem", "level": len(p[1][0]), "content": p[1][1]}

    def p_text(self, p):
        "text : TEXT"
        p[0] = {"type": "text", "content": p[1]}

    def p_task(self, p):
        "task : TASK"
        p[0] = {"type": "task", "content": p[1]}

    def p_label(self, p):
        "label : LABEL"
        p[0] = {"type": "label", "content": p[1]}

    def p_error(self, p):
        print(f"Syntax error at '{p.value}'")

    def parse(self, data):
        return self.parser.parse(data)
