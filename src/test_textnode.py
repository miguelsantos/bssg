import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev)")
        node2 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev)")
        self.assertEqual(node, node2)

    def test_not_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_link(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev)")
        node2 = TextNode("This is some anchor text", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq_normal_bold(self):
        node = TextNode("This is some text", TextType.NORMAL)
        node2 = TextNode("This is some text", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
