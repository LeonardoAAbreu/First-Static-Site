import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class BlockNode:
    def __init__(self, text_block, block_type):
        self.text_block = text_block
        self.block_type = block_type


def block_to_blocktype(text_block):
    if re.search(r"((?<!#)#{1,6} (?!#))", text_block):
        return BlockType.HEADING

    if re.search(r"(```[\s\S]*?```)", text_block):
        return BlockType.CODE

    if re.search(r">.*", text_block):
        return BlockType.QUOTE

    if re.search(r"- .*", text_block):
        return BlockType.UNORDERED_LIST

    if re.search(r"\d\..*", text_block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
