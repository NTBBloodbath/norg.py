from ply import lex


class NorgLexer:
    tokens = ("HEADING", "LISTITEM", "TEXT", "NEWLINE", "TASK", "LABEL")

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def t_HEADING(self, t):
        r"\*+ .*\n"
        t.value = t.value.strip().split(" ", 1)
        return t

    #  TODO: (vsedov) (05:15:11 - 31/05/23): Forgot to deal with the -- ----
    #  level of lists o_o
    def t_LISTITEM(self, t):
        r"(\-|\~)+ .*\n"
        t.value = t.value.strip().split(" ", 1)
        return t

    def t_TASK(self, t):
        r"\(\w\)\s.*\n"
        t.value = t.value.strip()
        return t

    def t_LABEL(self, t):
        r"[\+\-\~]\s.*\n"
        t.value = t.value.strip()
        return t

    def t_TEXT(self, t):
        r"[^\n]*\n"
        t.value = t.value.strip()
        return t

    def t_NEWLINE(self, t):
        r"\n"
        pass

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
