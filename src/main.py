from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    normal_text_node = TextNode("some text", TextType.NORMAL, None)
    link_text_node =  TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev)")
    # print(normal_text_node)
    print(link_text_node)
    html_node = HTMLNode("a", "boot.dev", props={"href": "https://google.com", "target": "_blank"})
    print(html_node)

if __name__ == '__main__':
    main()
