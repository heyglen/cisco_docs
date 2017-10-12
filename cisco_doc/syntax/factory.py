
import bs4

from cisco_doc.base_factory import BaseFactory
from cisco_doc.parser_settings import parser
from cisco_doc.syntax.option import Option
from cisco_doc.syntax.keyword import Keyword


class SyntaxFactory(BaseFactory):

    @classmethod
    def build(cls, section):
        all_syntax = section.find_all(
            parser.nxos.command.syntax.element,
            class_=parser.nxos.command.syntax.class_
        )

        cleaned_syntax = list()
        for syntax in all_syntax:
            cleaned = cls._clean(syntax)
            cleaned_syntax = cleaned_syntax + cleaned
        return cleaned_syntax

