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
    OPTIONAL_START = '['
    OPTIONAL_END = ']'


ALL_SYNTAX_TOKENS = [
    SYNTAX_TOKEN.OPTION_SEPARATOR,
    SYNTAX_TOKEN.OPTION_START,
    SYNTAX_TOKEN.OPTION_END,
    SYNTAX_TOKEN.OPTIONAL_START,
    SYNTAX_TOKEN.OPTIONAL_END,
]


class SyntaxFactory(BaseFactory):

    @classmethod
    def _clean_tokens(cls, tokens):
        cleaned_tokens = list()
        for token in tokens:
            token = cls._clean_element(token)
            if token is None:
                continue

            if isinstance(token, str):
                # '} {' -> '}' '{'
                # 'asdf}' -> 'asdf' '}'
                for find in ALL_SYNTAX_TOKENS:
                    token = token.replace(find, f' {find} ')
                    token = token.replace('  ', ' ')
                    token = token.strip()

                keywords_so_far = ''
                for part in token.split():
                    if part in ALL_SYNTAX_TOKENS:
                        if keywords_so_far:
                            cleaned_tokens.append(keywords_so_far)
                            keywords_so_far = ''
                        cleaned_tokens.append(part)
                    else:
                        keywords_so_far = f'{keywords_so_far} {part}'
                if keywords_so_far:
                    cleaned_tokens.append(keywords_so_far)
                token = token.strip()
                continue
            cleaned_tokens.append(token)
        return cleaned_tokens

    @classmethod
    def _parse_tokens(cls, tokens):
        parsed_tokens = list()
        for token in tokens:
            text = token if isinstance(token, str) else str(token)
            # logger.debug(f"Token 1: '{text}'")

            if token in ALL_SYNTAX_TOKENS:
                parsed_tokens.append(token)
            else:
                value = cls._parse_value(token)
                if value is None:
                    parsed_tokens.append(token)
                else:
                    parsed_tokens.append(value)
                    # raise ValueError(f'Unknown token {token}')
        return parsed_tokens

    @classmethod
    def _parse(cls, tokens):

        tokens = cls._clean_tokens(tokens)
        tokens = cls._parse_tokens(tokens)


        text = ' '.join([str(t) for t in tokens])
        logger.debug(f"Syntax: {text}")
        return tokens

        # for token in tokens:
        #     text = token if isinstance(token, str) else str(token)

        #     logger.debug(f"Token: '{text}'")
        #     logger.debug(f"Syntax: '{root}'")

        #     if token == SYNTAX_TOKEN.OPTIONAL_START:
        #         optional = True
        #     elif token == SYNTAX_TOKEN.OPTIONAL_END:
        #         optional = False
        #     elif token == SYNTAX_TOKEN.OPTION_START:
        #         parent = current
        #         stack.append(parent)
        #         current = Syntax()
        #         parent.append(current)
        #     elif token == SYNTAX_TOKEN.OPTION_END:
        #         current = stack.pop()
        #     elif token == SYNTAX_TOKEN.OPTION_SEPARATOR:
        #         parent = stack.pop()
        #         current = Syntax()
        #         parent.append(current)
        #     elif isinstance(token, (Keyword, Argument)):
        #         token.optional = optional
        #         current.append(token)
        # return root

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
        for index, command in enumerate(commands):
            cmd = cls._parse(command)
            parsed.append(cmd)
            if index > 3:
                break
        return parsed