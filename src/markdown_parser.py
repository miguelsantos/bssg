import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        intermediate_nodes = []
        parts = old_node.text.split(delimiter)

        # if only one part, no delimiter found, append the original node
        if len(parts) == 1:
            new_nodes.append(old_node)
            continue
        if len(parts) % 2 == 0:
            raise Exception("invalid markdown syntax: missing closing delimiter")

        for i, part in enumerate(parts):
            # even indexed parts are outside delimiters, append them as TextNodes of type TextType.TEXT
            if (i % 2) == 0:
                intermediate_nodes.append(TextNode(part, TextType.TEXT))

            # valid odd numbered parts are inside delimiters, append them as TextNode of tyepe text_type
            else:
                intermediate_nodes.append(TextNode(part, text_type))

        new_nodes.extend(intermediate_nodes)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
