from src.norg.abstract.actions import ConcatAction, IdentityAction, Terminal

"""
In this file, we contain the core structure of the headers, and core modules.

This is a modular creation of the parser.
"""

DOCUMENT_STRUCTURE = [
    ConcatAction("Header", ["heading", "title", "text"]),
    ConcatAction("LIST", ["list", "text"]),
    ConcatAction("AT", ["at_block", "at_language", "text", "at_end"]),
    IdentityAction("TEXT", ["text"]),
]
test_1 = """
@code pointer
@end
""".strip()

#     ╭────────────────────────────────────────────────────────────────────╮
#     │ Thank gpt for dealing with the regex crap                          │
#     ╰────────────────────────────────────────────────────────────────────╯
TERMINAL_PATTERNS = {
    "heading": r"\*+",
    "title": r"[^\n\r]+",
    "list": r"\-+",
    "at_block": r"\@+",
    "at_language": r"[^\n\r]+",
    "at_end": r"@end",
    "text": r"[^@\*\-]+",
}


TERMINALS = {
    name: Terminal(pattern) for name, pattern in TERMINAL_PATTERNS.items()
}
