import unittest

from blocknode import BlockNode, BlockType, block_to_blocktype


class TestBlockNodes(unittest.TestCase):
    def test_heading(self):
        new_block = BlockNode("#### The Lord of The Rings", BlockType.HEADING)
        test_case = block_to_blocktype(new_block.text_block)

        self.assertEqual(test_case, BlockType.HEADING)

    def test_code(self):
        new_block = BlockNode("```system.out.println('Hello World')```", BlockType.CODE)
        test_case = block_to_blocktype(new_block.text_block)

        self.assertEqual(test_case, BlockType.CODE)

    def test_quote(self):
        new_block = BlockNode("> You shall not pass", BlockType.QUOTE)
        test_case = block_to_blocktype(new_block.text_block)

        self.assertEqual(test_case, BlockType.QUOTE)
