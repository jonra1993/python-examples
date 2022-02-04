# https://www.naept.com/en/blog/a-simple-tree-building-algorithm/
from collections import deque
from typing import List

class RFNode:
    id: str = ''
    source: str = ''
    target: str = ''
    type: str = ''


def make_tree(nodes: List[RFNode], parent_id: str) -> List:
    populated = filter(lambda datum: datum['source'] == parent_id, nodes)
    origin_dest = []
    for i, value in enumerate(populated):
        origin_dest.append({
            **value,
            'children': make_tree(nodes, value['target'])
        })

    return origin_dest

# Recursive function to find paths from the root node to every leaf node
def get_root_to_leaf_paths(node: dict, path: deque, persistant_paths: deque):
    # include the current node to the path
    path.append({'source': node['source'], 'target': node['target'], 'id': node['id']})    

    # if a leaf node is found, print the path
    if is_node_leaf(node):
        persistant_paths.append(list(path))
        # print(list(path))
    else:
        for i, ro in enumerate(node['children']):
            get_root_to_leaf_paths(ro, path, persistant_paths)

    # backtrack: remove the current node after the left, and right subtree are done
    path.pop()

# The main function to get paths from the root node to every leaf node
def get_root_to_leaf_path(root: List[dict]):
    # list to store root-to-leaf path
    path = deque()
    persistant_paths = deque()
    for i, item in enumerate(root):
        get_root_to_leaf_paths(item, path, persistant_paths)

    data = []
    for i, item_list in enumerate(list(persistant_paths)):
        literal = []
        for j, item in enumerate(item_list):
            literal.append(item['source'])
            if is_last_element(item_list, j):
                literal.append(item['target'])
                            
        data.append(literal)        

    return data        
    

# Function to check if a given node is a leaf node or not
def is_node_leaf(path: dict):
    return len(path['children']) < 1


def is_last_element(elements: List[str], index: int):
    return len(elements) - 1 == index


def main():
    data = [
        {'id': 'e1-1.1', 'source': '1', 'target': '1.1', 'type': 'edge'},
        {'id': 'e1-1.2', 'source': '1', 'target': '1.2', 'type': 'edge'},
        {'id': 'e1.2-1.2.1', 'source': '1.2', 'target': '1.2.1', 'type': 'edge'},
        {'id': 'e1.2-1.2.2', 'source': '1.2', 'target': '1.2.2', 'type': 'edge'},
        {'id': 'e1-1.3', 'source': '1', 'target': '1.3', 'type': 'edge'},
        {'id': 'e1-2', 'source': '1', 'target': '2', 'type': 'edge'},
        {'id': 'e1-3', 'source': '1', 'target': '3', 'type': 'edge'},
        {'id': 'e3-3.1', 'source': '3', 'target': '3.1', 'type': 'edge'},
        {'id': 'e3-3.2', 'source': '3', 'target': '3.2', 'type': 'edge'},
        {'id': 'e3.1-3.1.1', 'source': '3.1', 'target': '3.1.1', 'type': 'edge'},
        {'id': 'e3.1-3.1.2', 'source': '3.1', 'target': '3.1.2', 'type': 'edge'},
    ]

    tree = make_tree(data, '1')
    paths = get_root_to_leaf_path(tree)
    print('persistant_paths', paths)


if __name__ == '__main__':
    main()
