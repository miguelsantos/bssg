class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        # HTML tag name string
        self.tag = tag
        # HTML tag value string
        self.value = value
        # HTML children list
        self.children = children
        # HTML props dict
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ''
        props_list = [""]
        for prop in self.props:
            props_list.append(f'{prop}="{self.props[prop]}"')

        return " ".join(props_list)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("invalid HTML: no value")
        if not self.tag:
            return self.value
        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("invalid HTML: no tag")
        if not self.children:
            raise ValueError("invalid HTML: no children")

        child_nodes = ""
        for child in self.children:
            child_nodes += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{child_nodes}</{self.tag}>"


    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"


