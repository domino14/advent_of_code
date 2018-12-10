from get_data import get_data

data = get_data(8)

# data = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
#       A----------------------------------
#           B----------- C-----------
#                            D-----
data = [int(d) for d in data.split(' ')]


class Node:
    def __init__(self, num_children, num_metadata):
        self.num_children = num_children
        self.num_metadata = num_metadata
        self.children = []  # Other nodes
        self.metadata = []
        self.value = 0


nodes = set()

metadata = 0


def read_node(data, left):
    global metadata
    if not data:
        return None, None
    n_children = data[left]
    n_metadata = data[left+1]
    left = left + 2
    node = Node(n_children, n_metadata)
    nodes.add(node)

    for c in range(n_children):
        child_node, new_left = read_node(data, left)
        if child_node is None:
            continue
        node.children.append(child_node)
        left = new_left
    # Once we're done reading the children, read metadata.
    node.metadata = data[left:left + n_metadata]
    if n_children == 0:
        node.value = sum(node.metadata)
    else:
        value = 0
        for meta in node.metadata:
            if meta == 0:
                continue
            meta -= 1
            try:
                value += node.children[meta].value
            except IndexError:
                pass
        node.value = value

    metadata += sum(node.metadata)
    return node, left + n_metadata


node, _ = read_node(data, 0)
print('1:', metadata)
print('2:', node.value)

