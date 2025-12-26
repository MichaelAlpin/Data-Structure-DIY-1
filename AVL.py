#id1:
#name1:
#username1:
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
    """Constructor, you are allowed to add more fields. 
    
    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """
    def __init__(self, key = None, value = None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """
    def is_real_node(self):
        return self.key != None
    
    """checks if the node is balanced
    
    @rtype: bool
    @returns: True if the node is balanced, False otherwise.
    """

    def is_balanced(self):
        return abs(self.balance_factor()) <= 1


    """calculates the balance factor of the node
    @rtype: int
    @returns: the balance factor of the node
    """
    def balance_factor(self):
        return self.left.height - self.right.height
    

    """updates the height of the node based on its children's heights
    """ 
    def update_height(self):
        self.height = 1 + max(self.left.height, self.right.height)

    """string representation of the node for debugging purposes
    @rtype: str
    @returns: a string representing the node
    """

    def __str__(self):
        return f"Key: {self.key}, val: {self.value}, Height: {self.height}"
"""
A class implementing an AVL tree.
"""

class AVLTree(object):

    """
    Constructor, you are allowed to add more fields.
    """
    def __init__(self):
        self.virtual_node = AVLNode()
        self.root = None
        self.tree_size = 0
        self.max = None

    

    """searches for a node in the dictionary corresponding to the key (starting at the root)
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def search(self, key):
        return self.__rec_search__(self.root, key, 0)

    """recursive search helper method - searching a key from a given node and calculating the path length
        
    @type key: int
    @type node: AVLNode
    @type path_len: int
    @param key: a key to be searched
    @param node: the currant node in the search
    @param path_len: the length of the path from the original node to the currant node
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def __rec_search__(self, node, key, path_len):
        if node is self.virtual_node or node is None:
            return None, path_len + 1
        if key == node.key:
            return node, path_len + 1
        if key < node.key:
            return self.__rec_search__(node.left, key, path_len + 1)
        return self.__rec_search__(node.right, key, path_len + 1)
    

    """searches for a node in the dictionary corresponding to the key, starting at the max
        
    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
    and e is the number of edges on the path between the starting node and ending node+1.
    """
    def finger_search(self, key):
        return None, -1


    """inserts a new node into the dictionary with corresponding key and value (starting at the root)
    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def insert(self, key, val):
        self.tree_size += 1
        if self.root is None or self.root is self.virtual_node:
            new_node = AVLNode(key, val)
            new_node.left = self.virtual_node
            new_node.right = self.virtual_node
            self.root = new_node
            self.max = new_node
            new_node.update_height()
            return new_node, 0, 0
        x, e = self.__rec_insert__(key, val, self.root, 0)
        if key > self.max.key:
            self.max = x
        h = self.__rebalace__(x.parent, 0)
        return x, e, h
    

    """recursive insert helper method - inserting a new node from a given node and calculating the path length
    *note: does not perform rebalancing*
    @type key: int
    @type val: string
    @type node: AVLNode
    @type path_len: int
    @param key: key of item that is to be inserted to self
    @param val: the value of the item
    @param node: the currant node in the insertion
    @param path_len: the length of the path from the original node to the currant node
    @rtype: (AVLNode,int)
    @returns: a tuple (x,e) where x and e are the described in the insert method
    """
    def __rec_insert__(self, key, val, node, path_len):
        if key < node.key:
            if node.left is self.virtual_node:
                new_node = AVLNode(key, val)
                new_node.left = self.virtual_node
                new_node.right = self.virtual_node
                node.left = new_node
                new_node.parent = node
                node.update_height()
                return new_node, path_len + 1
            new_node, path_len = self.__rec_insert__(key, val, node.left, path_len + 1)
        else:
            if node.right is self.virtual_node:
                new_node = AVLNode(key, val)
                new_node.left = self.virtual_node
                new_node.right = self.virtual_node
                node.right = new_node
                new_node.parent = node
                node.update_height()
                return new_node, path_len + 1
            new_node, path_len = self.__rec_insert__(key, val, node.right, path_len + 1)
        return new_node, path_len


    """performs a left rotation on the given node

    @type node: AVLNode
    @param node: the node to perform the rotation on
    @rtype: AVLNode
    @returns: the new root of the subtree after rotation
    """

    def __right_rotate__(self, node):
        left_child = node.left
        parent = node.parent
        node.left = left_child.right
        if not left_child is self.virtual_node:
            left_child.right.parent = node
        left_child.right = node
        node.parent = left_child
        left_child.parent = parent
        if parent is None:
            self.root = left_child
        else:
            if parent.left == node:
                parent.left = left_child
            else:
                parent.right = left_child
        node.update_height()
        left_child.update_height()
        return left_child


    """performs a left rotation on the given node
    @type node: AVLNode
    @param node: the node to perform the rotation on
    @rtype: AVLNode
    @returns: the new root of the subtree after rotation
    """

    def __left_rotate__(self, node):
        right_child = node.right
        parent = node.parent
        node.right = right_child.left
        if right_child is not self.virtual_node:
            right_child.left.parent = node
        right_child.left = node
        node.parent = right_child
        right_child.parent = parent
        if parent is None:
            self.root = right_child
        else:
            if parent.left == node:
                parent.left = right_child
            else:
                parent.right = right_child
        node.update_height()
        right_child.update_height()
        return right_child
    
    """performs a left-right rotation on the given node

    @type node: AVLNode
    @param node: the node to perform the rotation on
    @rtype: AVLNode
    @returns: the new root of the subtree after rotation
    """

    def __left_right_rotate__(self, node):
        node.left = self.__left_rotate__(node.left)
        return self.__right_rotate__(node)
    
    """performs a right-left rotation on the given node

    @type node: AVLNode
    @param node: the node to perform the rotation on
    @rtype: AVLNode
    @returns: the new root of the subtree after rotation
    """

    def __right_left_rotate__(self, node):
        node.right = self.__right_rotate__(node.right)
        return self.__left_rotate__(node)
    
    """inserts a new node into the dictionary with corresponding key and value, starting at the max

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int)
    @returns: a 3-tuple (x,e,h) where x is the new node,
    e is the number of edges on the path between the starting node and new node before rebalancing,
    and h is the number of PROMOTE cases during the AVL rebalancing
    """
    def finger_insert(self, key, val):
        return None, -1, -1

    def __rebalace__(self, node, counter = 0):
        if node is None:
            return counter
        old_hight = node.height
        node.update_height()
        if node.is_balanced():
            if old_hight != node.height:
                return self.__rebalace__(node.parent, counter)
            else:
                return counter
        if node.balance_factor() == 2:
            if node.left.balance_factor() == 1:
                self.__right_rotate__(node)
            else:
                self.__left_right_rotate__(node)
        if node.balance_factor() == -2:
            if node.right.balance_factor() == -1:
                self.__left_rotate__(node)
            else:
                self.__right_left_rotate__(node)
        counter += 1
        node.update_height()
        return self.__rebalace__(node.parent, counter)

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """
    def delete(self, node):
        return	

    
    """joins self with item and another AVLTree

    @type tree2: AVLTree 
    @param tree2: a dictionary to be joined with self
    @type key: int 
    @param key: the key separting self and tree2
    @type val: string
    @param val: the value corresponding to key
    @pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
    or the opposite way
    """
    def join(self, tree2, key, val):
        return


    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: the node in the dictionary to be used for the split
    @rtype: (AVLTree, AVLTree)
    @returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    """
    def split(self, node):
        return None, None

    
    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """
    def avl_to_array(self):
        arr = self.__inorder__(self.root, [])
        return arr


    """inorder traversal helper method for avl_to_array"""
    def __inorder__(self, node, arr):
        if node is self.virtual_node:
            return
        self.__inorder__(node.left, arr)
        arr.append((node, node.value))
        self.__inorder__(node.right, arr)
        return arr


    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self):
        return self.max

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        return self.tree_size	


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root
