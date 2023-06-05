import pytest

from src.norg.document_structure import DOCUMENT_STRUCTURE, TERMINAL_PATTERNS
from src.norg.grammar.grammar import GrammarGenerator
from src.norg.parser import ParserCore


@pytest.fixture
def parser():
    quick_test = GrammarGenerator(DOCUMENT_STRUCTURE, TERMINAL_PATTERNS)
    grammar = quick_test.parser(False)
    return ParserCore(grammar)


def test_header_1_with_fixture(printer, parser):
    test_1 = """
    * Heading 1.2
    Content 1.1
    content 1.2
    ** Heading 2 pointer
    I am a god
    """.strip()
    expected_1 = """
document[0->85]
  document_g1_0[0->85]
    document_g1_1[0->85]
      document_g1_1[0->50]
        document_g1[0->50]
          Header[0->50]
            heading[0->1, "*"]
            title[1->13, " Heading 1.2"]
            text[13->50, "
    Content 1.1
    content 1.2
    "]
      document_g1[50->85]
        Header[50->85]
          heading[50->52, "**"]
          title[52->70, " Heading 2 pointer"]
          text[70->85, "
    I am a god"]
    """.strip()
    assert (
        parser.parse(test_1).get_nonlazy_tree().to_str().strip() == expected_1
    )


def test_header_2_with_fixture(printer, parser):
    test_2 = """
    * Heading 1
        The content of Header 1
        ** Heading 2
        The content of Header 2
            *** Header 3
            The content of Header 3
            **** Header 4
            The content of Header 4
            ***** Header 5
    Out of indent header 5 content ?
    This would be a good test, how does it handle this thing ?
    """.strip()
    expected_2 = """
document[0->346]
  document_g1_0[0->346]
    document_g1_1[0->346]
      document_g1_1[0->232]
        document_g1_1[0->170]
          document_g1_1[0->109]
            document_g1_1[0->52]
              document_g1[0->52]
                Header[0->52]
                  heading[0->1, "*"]
                  title[1->11, " Heading 1"]
                  text[11->52, "
        The content of Header 1
        "]
            document_g1[52->109]
              Header[52->109]
                heading[52->54, "**"]
                title[54->64, " Heading 2"]
                text[64->109, "
        The content of Header 2
            "]
          document_g1[109->170]
            Header[109->170]
              heading[109->112, "***"]
              title[112->121, " Header 3"]
              text[121->170, "
            The content of Header 3
            "]
        document_g1[170->232]
          Header[170->232]
            heading[170->174, "****"]
            title[174->183, " Header 4"]
            text[183->232, "
            The content of Header 4
            "]
      document_g1[232->346]
        Header[232->346]
          heading[232->237, "*****"]
          title[237->246, " Header 5"]
          text[246->346, "
    Out of indent header 5 content ?
    This would be a good test, how does it handle this thing ?"]
        """.strip()
    assert (
        parser.parse(test_2).get_nonlazy_tree().to_str().strip() == expected_2
    )
