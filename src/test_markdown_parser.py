import unittest

from textnode import TextNode, TextType
from markdown_parser import *


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

class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_images_at_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_at_beginning(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) before text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" before text", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_images_2_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_at_end(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
            ],
            new_nodes,
        )

    def test_split_unbalanced_link(self):
        node = TextNode("text with unbalanced link [unbalanced link](www.unbalanced.com", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("text with unbalanced link [unbalanced link](www.unbalanced.com", TextType.TEXT)],
            new_nodes
        )

    def test_split_images_image_and_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a link [link](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_surrounded_by_text(self):
        node = TextNode("text [link](link.com) text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "link.com"),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_all_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )


    def test_empy_text(self):
        text = ""
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("", TextType.TEXT)], new_nodes)

    def test_only_text(self):
        text = "this is only text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("this is only text", TextType.TEXT)], new_nodes)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_text(self):
        md = """"""
        blocks = markdown_to_blocks(md)
        self.assertEqual([], blocks)

    def test_excessive_newlines(self):
        md = """
This is **bolded** paragraph

Another **bolded** paragraph


Paragraph after 2 newlines



Paragraph after 3 newlines
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual([
            "This is **bolded** paragraph",
            "Another **bolded** paragraph",
            "Paragraph after 2 newlines",
            "Paragraph after 3 newlines",
        ], blocks)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        blocks = [
            "# h1",
            "## h2",
            "### h3",
            "#### h4",
            "##### h5",
            "###### h6",
        ]
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertListEqual([
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
        ], block_types)

    def test_code(self):
        blocks = [
            """```
code
```""",
"""```code```""",
"""```code
```""",
"""```
code```""",
        ]
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertListEqual([
            BlockType.CODE,
            BlockType.CODE,
            BlockType.CODE,
            BlockType.CODE,
            ], block_types)

    def test_quote(self):
        blocks = [
            ">quoted line 1\n> quoted line 2\n>quoted line 3",
            ">quoted line 1\nnon quoted line\n>quoted line 2",
        ]
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertListEqual([
            BlockType.QUOTE,
            BlockType.PARAGRAPH,
        ], block_types)

    def test_ulist(self):
        blocks = [
            "- ulist line 1\n- ulist line 2\n- ulist line 3",
            "- ulist line 1\nnormal line\n- ulist line 2",
        ]
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertListEqual([
            BlockType.UNORDERED_LIST,
            BlockType.PARAGRAPH,
        ], block_types)

if __name__ == '__main__':
    unittest.main()
