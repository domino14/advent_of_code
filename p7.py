from get_data import get_data, get_data_lines

data = get_data_lines(7)

# data ="""Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin.""".split('\n')


steps = []
for line in data:
    words = line.split(' ')
    first_step = words[1]
    second_step = words[7]
    steps.append((first_step, second_step))

total_workers = 5

class Node:
    constant_cost = 60

    def __init__(self, name):
        self.name = name
        self.children = []
        self.parents = []
        self.performed = False
        self.performing = False
        self.time_to_perform = self.constant_cost + ord(name) - ord('A') + 1
        self.time_left = self.time_to_perform

    def parents_performed(self):
        for p in self.parents:
            if p.performed is False:
                return False
        return True

    def __str__(self):
        return (f'<{self.name}: {[c.name for c in self.children]}  '
                f'(parents: {[c.name for c in self.parents]})>')

    def __repr__(self):
        return self.__str__()


node_dict = {}


for step_desc in steps:
    parent = step_desc[0]
    child = step_desc[1]
    # print('parent', parent, 'child', child)
    if parent not in node_dict:
        node_dict[parent] = Node(parent)

    if child not in node_dict:
        child_node = Node(child)
        node_dict[child] = child_node

    node_dict[parent].children.append(node_dict[child])
    node_dict[child].parents.append(node_dict[parent])


for node in node_dict.values():
    node.children.sort(key=lambda n: n.name)
    node.parents.sort(key=lambda n: n.name)


print(node_dict)
# this is a tree.


order = []

while True:
    for step in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if step not in node_dict:
            continue
        if node_dict[step].parents_performed() and not node_dict[step].performed:
            node_dict[step].performed = True
            order.append(step)
            break
    if len(order) == len(node_dict):
        break

print('1: ', ''.join(order))

# Reset nodes and order for part 2
for n in node_dict:
    node_dict[n].performed = False
order = []
busy_workers = 0
seconds = 0
while True:
    modified_secs = False

    for step in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if step not in node_dict:
            continue
        print('checking step', step)
        if node_dict[step].parents_performed() and not node_dict[step].performed and not node_dict[step].performing:
            if busy_workers < total_workers:
                print('# free workers', total_workers-busy_workers, 'assign to task', step)
                busy_workers += 1
                node_dict[step].performing = True

    for step in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if step not in node_dict:
            continue
        if node_dict[step].performing:
            modified_secs = True
            node_dict[step].time_left -= 1
            print('time left on task', step, node_dict[step].time_left)

            if node_dict[step].time_left == 0:
                busy_workers -= 1
                node_dict[step].performed = True
                node_dict[step].performing = False
                print('task', step, 'is done. freeing worker, mark as performed')
                order.append(step)
                # break
            # break
    if modified_secs:
        seconds += 1
    print('time elapsed', seconds)
    if len(order) == len(node_dict):
        break

print('2: ', seconds)

# def traverse(node, order=order):
#     node.performed = True
#     if len(node.children) == 0:
#         return
#     for child in node.children:
#         if all([p.performed for p in child.parents]):
#             if not child.performed:
#                 order.append(child.name)
#                 child.performed = True
#             traverse(child, order)


# node_name_set = set(node_dict.keys())

# # Find the head node?
# for name, node in node_dict.items():
#     for child in node.children:
#         if child.name in node_name_set:
#             node_name_set.remove(child.name)

# print('parentless nodes: ', sorted(list(node_name_set)))

# for name in sorted(list(node_name_set)):
#     print('name', name, 'order', order)
#     order.append(name)

#     traverse(node_dict[name], order)


# not AVJDLXEFKBWCQUNGORTMYSIHPZ
#     AVJDLXEFKBWCQUNGORTMYSIHPZ