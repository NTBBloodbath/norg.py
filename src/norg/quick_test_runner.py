import re

from src.norg.document_structure import DOCUMENT_STRUCTURE, TERMINAL_PATTERNS
from src.norg.grammar.grammar import GrammarGenerator
from src.norg.parser import ParserCore


def test():
    test_1 = """
    * Heading 1
    @code math
    @end
    @code b
    pointer this is inside b
    @end
    """.strip()

    quick_test = GrammarGenerator(DOCUMENT_STRUCTURE, TERMINAL_PATTERNS)
    grammar = quick_test.parser(False)
    parser = ParserCore(grammar)

    parse_1 = parser.parse(test_1)
    print(parse_1.get_nonlazy_tree().to_str().strip())
    expected_1 = """
document[0->87]
  document_g1_0[0->87]
    document_g1_1[0->87]
      document_g1_1[0->40]
        document_g1_1[0->35]
          document_g1_1[0->16]
            document_g1[0->16]
              Header[0->16]
                heading[0->1, "*"]
                title[1->11, " Heading 1"]
                text[11->16, "
    "]
          document_g1[16->35]
            AT[16->35]
              at_block[16->17, "@"]
              at_language[17->26, "code math"]
              text[26->31, "
    "]
              at_end[31->35, "@end"]
        document_g1[35->40]
          TEXT[35->40]
            text[35->40, "
    "]
      document_g1[40->87]
        AT[40->87]
          at_block[40->41, "@"]
          at_language[41->48, "code b "]
          text[48->83, "
    pointer this is inside b
    "]
          at_end[83->87, "@end"]
    """.strip()
    print(expected_1)


if __name__ == "__main__":
    test()
