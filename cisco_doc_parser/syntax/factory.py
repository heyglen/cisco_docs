
import bs4

from cisco_doc_parser.syntax.option import Option
from cisco_doc_parser.syntax.keyword import Keyword


class SyntaxFactory:

    @classmethod
    def _clean(cls, syntax):
        cleaned = list()
        for element in syntax:
            if isinstance(element, bs4.element.NavigableString):
                # Empty String
                element = element.string.strip()
                if not element:
                    continue
            elif isinstance(element, bs4.element.Tag):
                # Page links
                if element.get('name', '').startswith('pgfId-'):
                    continue
            cleaned.append(element)
        return cleaned

    @classmethod
    def build(cls, syntax):
        syntax = cls._clean(syntax)
