import unittest

from textnode import TextNode, TextType
from markdown_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), expected)

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_just_delimited_italic_text(self):
        node = TextNode("_italic text_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode('', TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode('', TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_not_text_type(self):
        node = TextNode("bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_text_without_delimiter(self):
        node = TextNode("just text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("just text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_unbalanced_delimiter(self):
        node = TextNode("text with unmatched _italic delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
            print(new_nodes)

    def test_single_node_sequential_bold_and_italic(self):
        node = TextNode("**bold** and _italic_ text", TextType.TEXT)
        new_italic_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("**bold** and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_italic_nodes, expected)
        new_bold_nodes = split_nodes_delimiter(new_italic_nodes, "**", TextType.BOLD)
        expected2 = [
            TextNode('', TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_bold_nodes, expected2)

    def test_multiple_code_delimited_texts(self):
        node = TextNode("contains 2 `code` marked `code sections`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("contains 2 ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" marked ", TextType.TEXT),
            TextNode("code sections", TextType.CODE),
            TextNode('', TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_no_image(self):
        matches = extract_markdown_images("This is text")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com)"
        )
        self.assertListEqual([("link", "https://i.imgur.com")], matches)

    def test_extract_markdown_links_no_url(self):
        matches = extract_markdown_links(
            "This is text with a [](https://i.imgur.com)"
        )
        self.assertListEqual([("", "https://i.imgur.com")], matches)

    def test_extract_markdown_links_no_link(self):
        matches = extract_markdown_links(
            "This is text with a [link]()"
        )
        self.assertListEqual([("link", "")], matches)

if __name__ == '__main__':
    unittest.main()
