import pytest

from src.norg.document_structure import DOCUMENT_STRUCTURE, TERMINAL_PATTERNS
from src.norg.grammar.grammar import GrammarGenerator
from src.norg.parser import ParserCore


@pytest.fixture
def parser():
    quick_test = GrammarGenerator(DOCUMENT_STRUCTURE, TERMINAL_PATTERNS)
    grammar = quick_test.parser(False)
    return ParserCore(grammar)


def test_at_multiple_blocks(printer, parser):
    test_1 = """
    * Heading 1
    @code math
    @end
    @code b
    pointer this is inside b
    @end
    """.strip()

    expected_1 = """
document[0->85]
  document_g1_0[0->85]
    document_g1_1[0->85]
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
      document_g1[40->85]
        AT[40->85]
          at_block[40->41, "@"]
          at_language[41->47, "code b"]
          text[47->81, "
    pointer this is inside b
    "]
          at_end[81->85, "@end"]

    """.strip()

    parse_1 = parser.parse(test_1)
    assert parse_1.get_nonlazy_tree().to_str() == expected_1
