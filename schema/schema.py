from bs4 import Tag


def build_schema(element: Tag, element_tag: str):
    return {'element': element, element_tag + '_attributes': element.attrs, element_tag + '_string': element.string, 'element_tag': element_tag}
