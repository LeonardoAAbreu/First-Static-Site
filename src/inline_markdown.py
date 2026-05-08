from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_list = []

    if old_nodes.text_type != TextType.TEXT:
        return_list.append(old_nodes)
    else:
        splitted = old_nodes.text.split(delimiter)
        odd = True
        for string in splitted:
            if odd:
                node = TextNode(string.strip(), TextType.TEXT)
                return_list.append(node)
                odd = False
            else:
                match delimiter:
                    case "*":
                        node = TextNode(string.strip(), TextType.BOLD)
                        return_list.append(node)
                        odd = True
                    case "'":
                        node = TextNode(string.strip(), TextType.CODE)
                        return_list.append(node)
                        odd = True
                    case "_":
                        node = TextNode(string.strip(), TextType.ITALIC)
                        return_list.append(node)
                        odd = True
                    case _:
                        raise Exception("invalid MarkDown syntax")

    return return_list
