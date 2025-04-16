from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_parser import BlockType, text_to_textnodes, markdown_to_blocks, block_to_block_type


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    print(blocks)
    nodes = ParentNode("div", [])
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.CODE:
                print(block.strip("```"))
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
