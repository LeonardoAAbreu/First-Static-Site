import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text(self):
        base_node = TextNode("This is a `coded` text node", TextType.TEXT)
        separated_list = split_nodes_delimiter([base_node], "`", TextType.TEXT)
        node1 = TextNode("This is a ", TextType.TEXT)
        node2 = TextNode("coded", TextType.CODE)
        node3 = TextNode(" text node", TextType.TEXT)
        self.assertEqual(separated_list, [node1, node2, node3])

    def test_code(self):
        base_node = TextNode("`print('Hello World!')`", TextType.CODE)
        separated_list = split_nodes_delimiter([base_node], "`", TextType.CODE)
        node1 = TextNode("`print('Hello World!')`", TextType.CODE)
        self.assertEqual(separated_list, [node1])
