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


nodes = set()

metadata = 0


def read_node(data, left):
    global metadata
    print(f'reading data array, left={left}')
    if not data:
        return None, None
    n_children = data[left]
    n_metadata = data[left+1]
    left = left + 2
    node = Node(n_children, n_metadata)
    print(f'Created node with n_children {n_children} n_metadata {n_metadata}')
    nodes.add(node)
    for c in range(n_children):
        print(f'Child {c}:')
        child_node, new_left = read_node(data, left)
        if child_node is None:
            continue
        node.children.append(child_node)
        left = new_left
    # Once we're done reading the children, read metadata.
    node.metadata = data[left:left + n_metadata]
    print(f'Assigning node metadata: {node.metadata}')
    metadata += sum(node.metadata)
    return node, left + n_metadata

node = read_node(data, 0)
print(metadata)

# def traverse(node):
#     for child in node.children:
#         traverse(node, sum(node.metadata) + sum(child.metadata))
#     return sum(node.metadata)
