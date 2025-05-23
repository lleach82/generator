import unittest
from splitblocks import markdown_to_blocks, block_to_block_type
from blocknode import BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = (
            "This is **bolded** paragraph\n\n"
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line\n\n"
            "- This is a list\n"
            "- with items"
        )
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_extra_newlines(self):
        md = "\n\n\nFirst block\n\n\nSecond block\n\n\n\nThird block\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["First block", "Second block", "Third block"],
        )

    def test_whitespace_only_blocks(self):
        md = "Line 1\n\n   \n\nLine 2\n\n\t\n\nLine 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Line 1", "Line 2", "Line 3"],
        )

    def test_single_block(self):
        md = "Only one block here, no extra spacing"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Only one block here, no extra spacing"],
        )

class TestBlockToBlockType(unittest.TestCase):

    def test_heading_block(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Subheading"), BlockType.HEADING)

    def test_code_block(self):
        block = "```\ndef foo():\n    return 'bar'\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> with two lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is a normal paragraph with some **bold** text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_lines_not_list(self):
        block = "- Item one\n2. Not a valid list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
