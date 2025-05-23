import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    img_pattern = r'!\[([^\]]+)\]\(([^)]+)\)'
    
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        for match in re.finditer(img_pattern, text):
            start, end = match.span()
            alt, url = match.groups()

            # Text before image
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.PLAIN))
            
            # Image node
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            last_index = end

        # Remaining text after last match
        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.PLAIN))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    link_pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        for match in re.finditer(link_pattern, text):
            start, end = match.span()
            label, url = match.groups()

            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.PLAIN))

            new_nodes.append(TextNode(label, TextType.LINK, url))
            last_index = end

        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.PLAIN))

    return new_nodes
