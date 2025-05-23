import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_bold_text(self):
        node = TextNode("This has **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_split_italic_text(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_delimiters(self):
        node = TextNode("Text with **bold** and _italic_ together", TextType.TEXT)
        step1 = split_nodes_delimiter([node], "**", TextType.BOLD)
        step2 = split_nodes_delimiter(step1, "_", TextType.ITALIC)
        self.assertEqual(step2, [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" together", TextType.TEXT),
        ])

    def test_no_delimiters(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])  # unchanged

    def test_non_plain_node_is_unchanged(self):
        node = TextNode("Bold already", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])  # non-plain should not be touched

    def test_code_backtick_text(self):
        node = TextNode("`Valar`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("", TextType.TEXT),
            TextNode("Valar", TextType.CODE),
            TextNode("", TextType.TEXT),
        ])


if __name__ == "__main__":
    unittest.main()
