# parser.py
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter
from extractlinks import split_nodes_image, split_nodes_link

def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.PLAIN)
    nodes = [initial_node]

    # Order matters: images → links → bold → italic
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes
