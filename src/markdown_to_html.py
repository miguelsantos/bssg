from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_parser import BlockType, text_to_textnodes, markdown_to_blocks, block_to_block_type


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = ParentNode("div", [])
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.CODE:
                nodes.children.append(code_to_html_node(block))
            case BlockType.PARAGRAPH:
                pass
            case BlockType.HEADING:
                pass
            case BlockType.QUOTE:
                pass
            case BlockType.ULIST:
                pass
            case BlockType.OLIST:
                pass
    return nodes

def code_to_html_node(markdown):
    text = markdown[4:-3] if markdown[3] == "\n" else markdown[3:-3]
    text_node = TextNode(text, TextType.TEXT)
    return ParentNode("pre",
                      [ParentNode("code",
                        [text_node_to_html_node(text_node)])])

