import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(html_node.props_to_html(), ' href="https://google.com" target="_blank"')

    def test_props_to_html_empty(self):
        empty_node = HTMLNode()
        self.assertEqual(empty_node.props_to_html(), '')

    def test_repr(self):
       node = HTMLNode("a", "b", children=None, props=None)
       self.assertEqual(str(node), "HTMLNode(a, b, children: None, None)")

       empty_node_with_props = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
       self.assertEqual(str(empty_node_with_props),
                        "HTMLNode(None, None, children: None, {'href': 'https://google.com', 'target': '_blank'})")

    def test_repr_empty(self):
        empty_node = HTMLNode()
        self.assertEqual(str(empty_node), "HTMLNode(None, None, children: None, None)")

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_value(self):
        node = LeafNode("", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_tag(self):
        node = LeafNode(tag=None, value="this is raw text")
        self.assertEqual(node.to_html(), "this is raw text")


    def test_leaf_to_html_a(self):
        node = LeafNode("a", "boot.dev", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">boot.dev</a>')

if __name__ == '__main__':
    unittest.main()
