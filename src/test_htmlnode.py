import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(html_node.props_to_html(), 'href="https://google.com" target="_blank"')

    def test_props_to_html_empty(self):
        empty_node = HTMLNode()
        self.assertEqual(empty_node.props_to_html(), '')

    def test_repr(self):
       node = HTMLNode("a", "b", children=None, props=None)
       self.assertEqual(str(node), "tag: a, value: b, children: 0, props: ")

       empty_node_with_children = HTMLNode(children=[HTMLNode(),HTMLNode()])
       self.assertEqual(str(empty_node_with_children), "tag: None, value: None, children: 2, props: ")

       empty_node_with_props = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
       self.assertEqual(str(empty_node_with_props),
                        'tag: None, value: None, children: 0, props: href="https://google.com" target="_blank"')

    def test_repr_empty(self):
        empty_node = HTMLNode()
        self.assertEqual(str(empty_node), "tag: None, value: None, children: 0, props: ")

if __name__ == '__main__':
    unittest.main()
