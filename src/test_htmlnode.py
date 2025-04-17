import unittest

from htmlnode import *

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_create_parent_with_no_children(self):
        with self.assertRaises(TypeError):
            parent_node = ParentNode("a")
        with self.assertRaisesRegex(ValueError, 'children'):
            parent = ParentNode("div", None)
            parent.to_html()

    def test_create_parent_witout_tag(self):
        with self.assertRaisesRegex(ValueError, 'tag'):
            child1 = LeafNode("b", "child1")
            child2 = LeafNode("a", "boot.dev", {"href": "https://www.boot.dev"})
            parent = ParentNode(None, [child1, child2])
            parent.to_html()

    def test_to_html_multiple_children(self):
        child1 = LeafNode("b", "child1")
        child2 = LeafNode("a", "boot.dev", {"href": "https://www.boot.dev"})
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            '<div><b>child1</b><a href="https://www.boot.dev">boot.dev</a></div>'
        )

    def test_to_html_with_multiple_grandchildren(self):
        grandchild1 = LeafNode("b", "grandchild1")
        child1 = ParentNode("span", [grandchild1])
        grandchild2 = LeafNode("a", "grandchild2.com", {"href": "https://grandchild2.com"})
        child2 = ParentNode("span", [grandchild2])
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent.to_html(),
            '<div><span><b>grandchild1</b></span><span><a href="https://grandchild2.com">grandchild2.com</a></span></div>'
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == '__main__':
    unittest.main()
