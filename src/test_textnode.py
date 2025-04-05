import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        bold_node = TextNode("This is a text node", TextType.BOLD)
        bold_node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(bold_node, bold_node2)

        link_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev)")
        link_node2 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev)")
        self.assertEqual(link_node, link_node2)

    def test_not_eq(self):
        bold_node = TextNode("This is a text node", TextType.BOLD)
        bold_node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(bold_node, bold_node2)

        link_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev)")
        link_node2 = TextNode("This is some anchor text", TextType.LINK)
        self.assertNotEqual(link_node, link_node2)

    def test_not_eq_normal_bold(self):
        node = TextNode("This is some text", TextType.TEXT)
        node2 = TextNode("This is some text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, url="www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link text node")
        self.assertEqual(html_node.props, {"href": "www.boot.dev"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, url="www.boot.dev/img.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.boot.dev/img.jpg", "alt": "This is an image node"})

if __name__ == "__main__":
    unittest.main()
