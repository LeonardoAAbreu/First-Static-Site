import re

from blocknode import BlockType, block_to_blocktype
from htmlnode import ParentNode, text_node_to_html_node
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


def markdown_to_html_node(markdown):
    md_block_list = markdown_to_blocks(markdown)
    md_list = []

    for md_block in md_block_list:
        block_type = block_to_blocktype(md_block)

        match block_type:
            case BlockType.PARAGRAPH:
                md_split = md_block.split("\n")
                return_string = " ".join(md_split)
                md_list.append(ParentNode("p", text_to_children(return_string)))

            case BlockType.CODE:
                return_string = md_block[4:-3]
                raw = TextNode(return_string, TextType.TEXT)
                code_html = text_node_to_html_node(raw)
                md_list.append(ParentNode("pre", [ParentNode("code", [code_html])]))

            case BlockType.QUOTE:
                list_md_block = md_block.split("\n")
                stripped = [line[2:] for line in list_md_block]
                return_string = " ".join(stripped)

                md_list.append(
                    ParentNode("blockquote", text_to_children(return_string))
                )

            case BlockType.HEADING:
                heading_count = 0

                for char in md_block:
                    if char == "#":
                        heading_count += 1
                    else:
                        break

                md_block = md_block[heading_count + 1 :]
                md_list.append(
                    ParentNode(f"h{heading_count}", text_to_children(md_block))
                )

            case BlockType.ORDERED_LIST:
                list_md_block = md_block.split("\n")
                return_list = []

                for element in list_md_block:
                    element = element[3:]
                    return_list.append(ParentNode("li", text_to_children(element)))
                md_list.append(ParentNode("ol", return_list))

            case BlockType.UNORDERED_LIST:
                list_md_block = md_block.split("\n")
                return_list = []

                for element in list_md_block:
                    element = element[2:]
                    return_list.append(ParentNode("li", text_to_children(element)))
                md_list.append(ParentNode("ul", return_list))

    return ParentNode("div", md_list)


def text_to_children(text):
    text_list = text_to_textnodes(text)
    html_list = []

    for lines in text_list:
        html_list.append(text_node_to_html_node(lines))

    return html_list
