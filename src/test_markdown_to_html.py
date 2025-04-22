import unittest

from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# h1

## h2

### h3

#### h4

##### h5

###### h6

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><h1>h1</h1><h2>h2</h2><h3>h3</h3><h4>h4</h4><h5>h5</h5><h6>h6</h6></div>",
            html

        )

    def test_quote(self):
        md = """
> this
>is a
> **bolded** quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><blockquote>this is a <b>bolded</b> quote</blockquote></div>",
            html
        )

    def test_ulist(self):
        md = """
- Item 1
- Item 2
- Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
            html
        )

    def test_olist(self):
        md = """
1. Item 1
2. Item 2
3. Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
            html
        )

    def test_all(self):
        self.maxDiff = None
        md = """
# **H1**

This is a normal
multiline paragraph (should appear as single line)

> this is an
> _italics_ containing
> quote

```
this is
2 line code
```

- **bold** ulist 1
- _italic_ ulist 2

1. [link1](google.com)
2. [link2](yahoo.com)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            '<div><h1><b>H1</b></h1><p>This is a normal multiline paragraph (should appear as single line)</p><blockquote>this is an <i>italics</i> containing quote</blockquote><pre><code>this is\n2 line code\n</code></pre><ul><li><b>bold</b> ulist 1</li><li><i>italic</i> ulist 2</li></ul><ol><li><a href="google.com">link1</a></li><li><a href="yahoo.com">link2</a></li></ol></div>',
            html
        )

if __name__ == '__main__':
    unittest.main()
