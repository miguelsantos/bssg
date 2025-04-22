import re

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
                nodes.children.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                nodes.children.append(heading_to_html_node(block))
            case BlockType.QUOTE:
                nodes.children.append(quote_to_html_node(block))
            case BlockType.ULIST:
                nodes.children.append(ulist_to_html_node(block))
            case BlockType.OLIST:
                nodes.children.append(olist_to_html_node(block))
    return nodes

def code_to_html_node(markdown):
    text = markdown[4:-3] if markdown[3] == "\n" else markdown[3:-3]
    text_node = TextNode(text, TextType.TEXT)
    return ParentNode("pre",
                      [ParentNode("code",
                        [text_node_to_html_node(text_node)])])

def paragraph_to_html_node(markdown):
    p_node = ParentNode("p", text_to_children(markdown))
    return p_node

def heading_to_html_node(markdown):
    level = -1
    for i in range(6):
        if markdown.startswith(f"{'#' * (i + 1)} "):
            level = i + 1
            break
    if level == -1:
        raise Exception("not a heading")
    text = markdown[level + 1:]
    h_node = ParentNode(f"h{level}", text_to_children(text))
    return h_node

def quote_to_html_node(markdown):
    text = ""
    for line in markdown.split(">"):
        text += line.removeprefix(" ")
    blockquote_node = ParentNode("blockquote", text_to_children(text))
    return blockquote_node

def ulist_to_html_node(markdown):
    ul_node = ParentNode("ul", [])
    items = [item.rstrip("\n") for item in markdown.split("- ") if item != '']
    for i in items:
        ul_node.children.append(ParentNode("li", text_to_children(i)))
    return ul_node

def olist_to_html_node(markdown):
    ol_node = ParentNode("ol", [])
    lines = re.split(r"^\d\. ", markdown, flags=re.MULTILINE)
    items = [item.rstrip("\n") for item in lines if item != '']
    for i in items:
        ol_node.children.append(ParentNode("li", text_to_children(i)))
    return ol_node

def text_to_children(text):
    nodes = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i != len(lines) - 1:
            line = line + " "
        for tnode in text_to_textnodes(line):
            nodes.append(text_node_to_html_node(tnode))
    return nodes
