
import bs4

from cisco_doc.parser_settings import parser


class BaseFactory:
    @classmethod
    def _clean(cls, elements):
        cleaned = list()
        anchor_prefix = parser.nxos.anchor_prefix
        for element in elements:
            # Ignore empty string
            if isinstance(element, bs4.element.NavigableString):
                if not element.string.strip():
                    continue
            # Ignore page anchors
            elif isinstance(element, bs4.element.Tag):
                name = element.get('name', '')
                if name.startswith(anchor_prefix):
                    continue
            cleaned.append(element)
        return cleaned
