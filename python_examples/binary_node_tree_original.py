from collections import deque
from multiprocessing.sharedctypes import Value
from typing import Iterable, List

# A class to store a binary tree node
class Node:
    def __init__(self, data: int, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


# Function to check if a given node is a leaf node or not
def is_leaf(node: Node):
    return node.left is None and node.right is None


# Recursive function to find paths from the root node to every leaf node
def print_root_to_leaf_paths(node: Node, path: deque):

    # base case
    if node is None:
        return

    # include the current node to the path
    path.append(node.data)

    # if a leaf node is found, print the path
    if is_leaf(node):
        print(list(path))

    # recur for the left and right subtree
    print_root_to_leaf_paths(node.left, path)
    print_root_to_leaf_paths(node.right, path)

    # backtrack: remove the current node after the left, and right subtree are done
    path.pop()

# The main function to print paths from the root node to every leaf node
def print_root_to_leaf_path(root: Node):

    # list to store root-to-leaf path
    path = deque()
    print_root_to_leaf_paths(root, path)

def main():
    ''' Construct the following tree
              1
            /   \
           /     \
          2       3
         / \     / \
        4   5   6   7
               /     \
              8       9
    '''
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)
    root.right.left.left = Node(8)
    root.right.right.right = Node(9)

    # print all root-to-leaf paths
    print_root_to_leaf_path(root)


if __name__ == '__main__':
    main()
