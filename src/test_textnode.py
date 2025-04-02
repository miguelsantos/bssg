import unittest

from textnode import TextNode, TextType


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
        node = TextNode("This is some text", TextType.NORMAL)
        node2 = TextNode("This is some text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.NORMAL, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, normal, https://www.boot.dev)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()
