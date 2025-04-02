class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        if not children:
            self.children = []
        else:
            self.children = children
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
