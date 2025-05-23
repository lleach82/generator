import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text

"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text</p></div>",
        )

    def test_heading(self):
        md = "# This is a heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>")

    def test_quote(self):
        md = "> Quote line one\n> Quote line two"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><blockquote>Quote line one Quote line two</blockquote></div>")

    def test_unordered_list(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>")

if __name__ == '__main__':
    unittest.main()