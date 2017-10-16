import logging

import bs4

from cisco_doc.base_factory import BaseFactory
from cisco_doc.parser_settings import parser
from cisco_doc.syntax.option import Option
from cisco_doc.syntax.argument import Argument
from cisco_doc.syntax.keyword import Keyword
from cisco_doc.syntax.syntax import Syntax
from cisco_doc.parser_settings import parser


logger = logging.getLogger(__name__)


class SYNTAX_TOKEN:
    OPTION_SEPARATOR = '|'
    OPTION_START = '{'
    OPTION_END = '}'


class SyntaxFactory(BaseFactory):

    @classmethod
    def _parse(cls, tokens):
        root = Syntax()

        current = root
        stack = [current]

        for token in tokens:

            token = cls._clean_element(token)
            if token is None:
                continue

            text = token if isinstance(token, str) else '\n' + token.prettify()
            logger.debug(f"Token: '{text}'")

            if token == SYNTAX_TOKEN.OPTION_START:
                parent = Syntax()
                new = Syntax()

                parent.append(new)
                current.append(parent)

                stack.append(parent)
                stack.append(new)

                current = new
            elif token == SYNTAX_TOKEN.OPTION_END:
                current = stack.pop()
                parent = stack.pop()
                previous = stack.pop()

                current = previous

            elif token == SYNTAX_TOKEN.OPTION_SEPARATOR:
                current = stack.pop()
                parent = stack.pop()

                new = Syntax()
                parent.append(new)

                stack.append(parent)
                stack.append(new)
                current = new
            else:
                value = cls._parse_value(token)
                if value is None:
                    raise ValueError(f'Unknown token {token}')
                current.append(value)
        return root

    @classmethod
    def _parse_value(cls, token):
        if isinstance(token, bs4.element.Tag):
            element_class = token.get('class', list())
            for class_name in parser.nxos.command.keyword.classes:
                if class_name in element_class:
                    return Keyword(token.string.strip())
            for class_name in parser.nxos.command.argument.classes:
                if class_name in element_class:
                    return Argument(token.string.strip())

    @classmethod
    def build(cls, section):
        commands = section.find_all(
            parser.nxos.command.syntax.element,
            class_=parser.nxos.command.syntax.class_
        )

        parsed = list()
        for command in commands:
            cmd = cls._parse(command)
            parsed.append(cmd)
        return parsed