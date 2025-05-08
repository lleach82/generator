from enum import Enum

class TextType(Enum):
    PLAIN = "Plain"
    BOLD = "Bold"
    ITALIC = "Italic"
    LINK = "Link"
    IMAGE = "Image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, alt):
        if isinstance(alt, TextNode):
            return (self.text == alt.text and 
                    self.text_type == alt.text_type and
                    self.url == alt.url)
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
