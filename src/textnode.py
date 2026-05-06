from enum import Enum


class TextType(Enum):
    TEXT = "simple"
    BOLD_TEXT = "**bold**"
    ITALIC_TEXT = "_italic_"
    CODE_TEXT = "'code'"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self == other

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
