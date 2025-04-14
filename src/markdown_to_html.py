from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_parser import BlockType, text_to_text_nodes, markdown_to_blocks, block_to_block_type


def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.CODE:
                pass
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
