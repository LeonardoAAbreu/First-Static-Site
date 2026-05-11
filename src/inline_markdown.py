import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_list = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            return_list.append(old_node)
        else:
            splitted = old_node.text.split(delimiter)
            odd = True
            for string in splitted:
                if odd:
                    node = TextNode(string, TextType.TEXT)
                    return_list.append(node)
                    odd = False
                else:
                    odd = True
                    match delimiter:
                        case "**":
                            node = TextNode(string, TextType.BOLD)
                            return_list.append(node)
                        case "`":
                            node = TextNode(string, TextType.CODE)
                            return_list.append(node)
                        case "_":
                            node = TextNode(string, TextType.ITALIC)
                            return_list.append(node)
                        case _:
                            raise Exception("invalid MarkDown syntax")

    return return_list


def extract_markdown_images(text):
    return_list = []
    return_list.extend(re.findall(r"!\[(.*?)\]\((.*?)\)", text))
    return return_list


def extract_markdown_links(text):
    return_list = []
    return_list.extend(re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text))
    return return_list


def split_nodes_image(old_nodes):
    return_list = []

    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT:
            return_list.append(nodes)

        else:
            remaining = nodes.text
            node_list = extract_markdown_images(remaining)

            for listed in node_list:
                image_alt, image_link = listed
                split_nodes = remaining.split(f"![{image_alt}]({image_link})", 1)

                if split_nodes[0]:
                    return_list.append(TextNode(split_nodes[0], TextType.TEXT))

                return_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if len(split_nodes) > 1:
                    remaining = split_nodes[1]

            if remaining:
                return_list.append(TextNode(remaining, TextType.TEXT))

    return return_list


def split_nodes_link(old_nodes):
    return_list = []

    for nodes in old_nodes:
        if nodes.text_type != TextType.TEXT:
            return_list.append(nodes)

        else:
            remaining = nodes.text
            node_list = extract_markdown_links(remaining)

            for listed in node_list:
                link_alt, link = listed
                split_nodes = remaining.split(f"[{link_alt}]({link})", 1)

                if split_nodes[0]:
                    return_list.append(TextNode(split_nodes[0], TextType.TEXT))

                return_list.append(TextNode(link_alt, TextType.LINK, link))
                if len(split_nodes) > 1:
                    remaining = split_nodes[1]

            if remaining:
                return_list.append(TextNode(remaining, TextType.TEXT))

    return return_list


def text_to_textnodes(text):
    return_list = [TextNode(text, TextType.TEXT)]

    return_list = split_nodes_delimiter(return_list, "**", TextType.BOLD)
    return_list = split_nodes_delimiter(return_list, "_", TextType.ITALIC)
    return_list = split_nodes_delimiter(return_list, "`", TextType.CODE)
    return_list = split_nodes_image(return_list)
    return_list = split_nodes_link(return_list)

    return return_list


def markdown_to_blocks(markdown):
    markdown_list = markdown.split("\n\n")
    return_list = []

    for mk in markdown_list:
        mk = mk.strip()
        if mk:
            return_list.append(mk)

    return return_list
