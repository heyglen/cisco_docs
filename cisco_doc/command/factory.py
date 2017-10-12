
import bs4

from cisco_doc.parser_settings import parser
from cisco_doc.command.command import Command
from cisco_doc.syntax.factory import SyntaxFactory
from cisco_doc.base_factory import BaseFactory

class CommandFactory(BaseFactory):

    @classmethod
    def _get_description(cls, section):
        description = section.find(
            parser.nxos.command.description.element,
            class_=parser.nxos.command.description.class_
        ).contents
        return cls._clean(description)

    @classmethod
    def build(cls, section):
        command = Command()
        for tag in section.h2.children:
            if isinstance(tag, bs4.element.NavigableString):
                command.name = tag
                break

        command.description = cls._get_description(section)
        command.syntax = SyntaxFactory.build(section)

        import ipdb; ipdb.set_trace()

        logger.debug(f'Command {command}')
        return command