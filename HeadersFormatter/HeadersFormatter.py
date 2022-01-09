from math import ceil

from anytree import Node

_excluded_strings = ["::"]
_alphabet = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm',
             14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: 'y',
             26: 'z'}


def format_for_anki(headers: Node, add_alphabet_numeration: bool):
    # Remove invalid strings from nodes names
    _remove_excluded_strings_from_names(headers)

    if add_alphabet_numeration:
        # Add alphabet numeration
        _add_alphabet_numeration_by_depth_and_order(0, headers)


def _remove_excluded_strings_from_names(headers: Node):
    # Remove invalid strings from name
    for excluded_string in _excluded_strings:
        headers.name = str.replace(headers.name, excluded_string, "-")

    if headers.is_leaf:
        return
    else:
        children = headers.children
        for child in children:
            _remove_excluded_strings_from_names(child)
        return


def _add_alphabet_numeration_by_depth_and_order(order_number: int, headers: Node):
    if not headers.is_root:
        # Make prefix
        prefix = ""

        number_prefixes = (order_number + 1) / len(_alphabet)
        if number_prefixes > 1:
            if number_prefixes > int(number_prefixes):
                number_prefixes = int(number_prefixes)
            else:
                number_prefixes = int(number_prefixes) - 1

            for i in range(int(number_prefixes)):
                prefix = prefix + "z"

        # Add a word to the name
        alphabet_index = order_number % len(_alphabet) + 1
        headers.name = prefix + _alphabet[alphabet_index] + " " + headers.name

    if headers.is_leaf:
        return
    else:
        children = headers.children
        for index in range(len(children)):
            _add_alphabet_numeration_by_depth_and_order(index, children[index])
        return
