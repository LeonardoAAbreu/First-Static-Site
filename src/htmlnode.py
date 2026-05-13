from textnode import TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # sem isso é só texto
        self.value = value  # sem isso tem filhos
        self.children = children  # sem isso tem valor
        self.props = props  # sem isso não tem atributos

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def to_html(self):
        if not self.value:
            raise ValueError

        if not self.tag:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def props_to_html(self):
        if not self.props:
            return ""

        return " ".join(f' {i}="{j}"' for i, j in self.props.items())


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=""):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError

        if not self.tag:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=""):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError

        if len(self.children) < 1:
            raise ValueError("missing child")

        return f"<{self.tag}{self.props_to_html()}>{''.join(x.to_html() for x in self.children)}</{self.tag}>"


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise Exception("not a valid type")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            this_prop = {"href": text_node.url}
            return LeafNode("a", text_node.text, this_prop)
        case TextType.IMAGE:
            this_prop = {"src": text_node.url, "alt": text_node.text}
            return LeafNode("img", "", this_prop)
