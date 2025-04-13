import re
from enum import Enum

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

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_images(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        intermediate_nodes = []
        original_text = old_node.text
        for image_alt, image_link in matches:
            # split text before and after current match
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections[0]) == 0:
                # text starts with image, append IMAGE TextNode first
                intermediate_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if len(matches) == 1:
                    # only 1 match, append second half of section as TEXT TextTNode
                    intermediate_nodes.append(TextNode(sections[1], TextType.TEXT))
                else:
                    # more than 1 match, set original_text as section after current match
                    original_text = sections[1]
            else:
                # append first split part as TEXT TextNode
                intermediate_nodes.append(TextNode(sections[0], TextType.TEXT))
                # append current match as IMAGE TextNode
                intermediate_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if len(matches) == 1:
                    if sections[1] != '':
                        # only 1 match, append second half of section as TEXT TextTNode
                        intermediate_nodes.append(TextNode(sections[1], TextType.TEXT))
                else:
                    # more than 1 match, set original_text as section after current match
                    original_text = sections[1]
                # # set original_text as the section after the current match
                # original_text = sections[1]
        new_nodes.extend(intermediate_nodes)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        matches = extract_markdown_links(old_node.text)
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue
        intermediate_nodes = []
        original_text = old_node.text
        for image_alt, image_link in matches:
            # split text before and after current match
            sections = original_text.split(f"[{image_alt}]({image_link})", 1)
            if len(sections[0]) == 0:
                # text starts with link, append LINK TextNode first
                intermediate_nodes.append(TextNode(image_alt, TextType.LINK, image_link))
                if len(matches) == 1:
                    # only 1 match, append second half of section as TEXT TextTNode
                    intermediate_nodes.append(TextNode(sections[1], TextType.TEXT))
                else:
                    # more than 1 match, set original text section after current match
                    original_text = sections[1]
            else:
                # append first split part as TEXT TextNode
                intermediate_nodes.append(TextNode(sections[0], TextType.TEXT))
                # append current match as LINK TextNode
                intermediate_nodes.append(TextNode(image_alt, TextType.LINK, image_link))
                if len(matches) == 1:
                    if sections[1] != '':
                        # only 1 match, append second half of section as TEXT TextTNode
                        intermediate_nodes.append(TextNode(sections[1], TextType.TEXT))
                else:
                    # more than 1 match, set original_text as section after current match
                    original_text = sections[1]
        new_nodes.extend(intermediate_nodes)
    return new_nodes


def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    split_bold = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_image = split_nodes_image(split_code)
    split_link = split_nodes_link(split_image)

    return split_link

def markdown_to_blocks(markdown):
    return list(filter(lambda b: b != '', map(lambda x: x.strip("\n"), markdown.split("\n\n"))))

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered"
    ORDERED_LIST = "ordered"

def block_to_block_type(block):
    if re.match(r"^#{1,6} .", block):
        return BlockType.HEADING
    elif block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    elif block[0] == ">":
        for line in block.split("\n"):
            if line[0] != ">":
                return BlockType.PARAGRAPH
            else:
                continue
        return BlockType.QUOTE
    elif block[0:2] == "- ":
        for line in block.split("\n"):
            if line[0:2] != "- ":
                return BlockType.PARAGRAPH
            else:
                continue
        return BlockType.UNORDERED_LIST
    else:
        return BlockType.PARAGRAPH
