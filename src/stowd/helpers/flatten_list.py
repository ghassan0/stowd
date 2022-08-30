"""
Create a flat list from a list of lists.
"""


def flatten_list(list_of_lists):
    """Create a flat list from a list of lists."""
    flat_list = []
    for a_list in list_of_lists:
        for item in a_list:
            flat_list.append(item)
    return flat_list
