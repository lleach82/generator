import unittest
from textnode import TextNode, TextType
from extractlinks import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestMarkdownExtractors(unittest.TestCase):

    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images("Text with ![image](https://i.imgur.com/img.png)")
        self.assertEqual(matches, [("image", "https://i.imgur.com/img.png")])

    def test_extract_markdown_images_multiple(self):
        text = "Here is ![one](https://img1.com) and ![two](https://img2.com)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("one", "https://img1.com"), ("two", "https://img2.com")])

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This text has no images.")
        self.assertEqual(matches, [])

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links("Click [here](https://example.com)")
        self.assertEqual(matches, [("here", "https://example.com")])

    def test_extract_markdown_links_multiple(self):
        text = "Go [Google](https://google.com) or [Bing](https://bing.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("Google", "https://google.com"), ("Bing", "https://bing.com")])

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("Just text, no links.")
        self.assertEqual(matches, [])

    def test_links_do_not_capture_images(self):
        text = "Look ![alt](https://img.com) and [link](https://link.com)"
        self.assertEqual(extract_markdown_images(text), [("alt", "https://img.com")])
        self.assertEqual(extract_markdown_links(text), [("link", "https://link.com")])

    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_multiple(self):
        node = TextNode(
            "![one](url1) middle ![two](url2) end",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode(" middle ", TextType.PLAIN),
                TextNode("two", TextType.IMAGE, "url2"),
                TextNode(" end", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        node = TextNode("No images here.", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_single(self):
        node = TextNode(
            "Text with a [link](https://example.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_multiple(self):
        node = TextNode(
            "[One](url1) and [Two](url2) and done.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("One", TextType.LINK, "url1"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("Two", TextType.LINK, "url2"),
                TextNode(" and done.", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("No links here.", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_links_and_images_are_separate(self):
        node = TextNode(
            "A link [text](url) and an ![image](img)",
            TextType.PLAIN,
        )
        links = split_nodes_link([node])
        images = split_nodes_image([node])
        self.assertTrue(any(n.text_type == TextType.LINK for n in links))
        self.assertTrue(any(n.text_type == TextType.IMAGE for n in images))

if __name__ == "__main__":
    unittest.main()
