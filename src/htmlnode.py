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
        props_list = []
        for k in self.props:
            props_list.append(f'{k}="{self.props[k]}"')

        return " ".join(props_list)

    def __repr__(self):
        return f"tag: {self.tag}, value: {self.value}, children: {len(self.children)}, props: {self.props_to_html()}"
