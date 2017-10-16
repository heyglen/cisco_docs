
import bs4

from cisco_doc.parser_settings import parser


class BaseFactory:
    _anchor_prefix = parser.nxos.anchor_prefix

    @classmethod
    def _clean(cls, elements):
        cleaned = list()
        for element in elements:
            element = cls._clean_element(element)
            if element is not None:
                cleaned.append(element)
        return cleaned

    @classmethod
    def _clean_element(cls, element):
        # Ignore empty string
        if isinstance(element, bs4.element.NavigableString):
            if not element.string.strip():
                return None
            element = str(element).strip()
        # Ignore page anchors
        elif isinstance(element, bs4.element.Tag):
            name = element.get('name', '')
            tag_class = element.get('class', '')
            if name.startswith(cls._anchor_prefix):
                return None
            elif 'cCp_CmdPlain' in tag_class:
                element = str(element.string).strip()
        return element
