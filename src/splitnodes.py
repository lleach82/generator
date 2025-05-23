from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue

        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise Exception("Invalid delimiter formatting in text node: unmatched delimiter")

        for i, segment in enumerate(split_text):
            if segment == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(segment, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(segment, text_type))

    return new_nodes