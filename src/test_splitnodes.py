import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_bold_text(self):
        node = TextNode("This has **bold** text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This has ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
        ])

    def test_split_italic_text(self):
        node = TextNode("This is _italic_ text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN),
        ])

    def test_multiple_delimiters(self):
        node = TextNode("Text with **bold** and _italic_ together", TextType.PLAIN)
        step1 = split_nodes_delimiter([node], "**", TextType.BOLD)
        step2 = split_nodes_delimiter(step1, "_", TextType.ITALIC)
        self.assertEqual(step2, [
            TextNode("Text with ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" together", TextType.PLAIN),
        ])

    def test_no_delimiters(self):
        node = TextNode("Just plain text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])  # unchanged

    def test_non_plain_node_is_unchanged(self):
        node = TextNode("Bold already", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])  # non-plain should not be touched

if __name__ == "__main__":
    unittest.main()
