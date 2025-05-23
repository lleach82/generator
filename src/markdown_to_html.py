from htmlnode import ParentNode
from splitblocks import markdown_to_blocks, block_to_block_type
from blocknode import BlockType
from htmlnode import LeafNode, text_node_to_html_node
from textnode import TextNode, TextType
from extractlinks import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from splitnodes import split_nodes_delimiter


def text_to_children(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    for delimiter, text_type in [("**", TextType.BOLD), ("*", TextType.ITALIC), ("_", TextType.ITALIC)]:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return [text_node_to_html_node(node) for node in nodes]


def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        paragraph_text = " ".join(block.splitlines()).strip()
        return ParentNode("p", text_to_children(paragraph_text))

    elif block_type == BlockType.HEADING:
        heading_level = len(block.split(" ")[0])  # Count #s
        heading_text = block[heading_level+1:].strip()
        return ParentNode(f"h{heading_level}", text_to_children(heading_text))

    elif block_type == BlockType.CODE:
        code_content = "\n".join(block.strip().split("\n")[1:-1]) + "\n"
        leaf = LeafNode("code", code_content)
        return ParentNode("pre", [leaf])

    elif block_type == BlockType.QUOTE:
        stripped = " ".join([line.lstrip()[1:].lstrip() for line in block.split("\n")])
        return ParentNode("blockquote", text_to_children(stripped))

    elif block_type == BlockType.UNORDERED_LIST:
        children = [ParentNode("li", text_to_children(line[2:])) for line in block.split("\n")]
        return ParentNode("ul", children)

    elif block_type == BlockType.ORDERED_LIST:
        children = [ParentNode("li", text_to_children(line.split(". ", 1)[1])) for line in block.split("\n")]
        return ParentNode("ol", children)

    else:
        raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
