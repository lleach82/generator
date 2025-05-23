from blocknode import BlockType

def markdown_to_blocks(markdown):
    raw_blocks = markdown.strip().split("\n\n")
    blocks = [block.strip() for block in raw_blocks if block.strip()]
    return blocks

def block_to_block_type(block):
    lines = block.strip().split("\n")

    if lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.CODE

    if lines[0].startswith("#"):
        hash_count = 0
        for char in lines[0]:
            if char == "#":
                hash_count += 1
            else:
                break
        if 1 <= hash_count <= 6 and lines[0][hash_count:hash_count+1] == " ":
            return BlockType.HEADING

    if all(line.strip().startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.strip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(
        line.strip().startswith(f"{i+1}. ") for i, line in enumerate(lines)
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH