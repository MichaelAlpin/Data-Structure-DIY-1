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
        return abs(self.left.height - self.right.height) <= 1


    """updates the height of the node based on its children's heights
    """ 
    def update_height(self):
        self.height = 1 + max(self.left.height, self.right.height)

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
        self.size = 0
        self.max_node = None

    

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
        if node.is_real_node() == False:
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
        return None, -1, -1
    
    def __rec_insert__(self, key, val, node, path_len):
        if node.is_real_node() == False:
            new_node = AVLNode(key, val)
            new_node.left = AVLNode(-1, None)
            new_node.right = AVLNode(-1, None)

            new_node.update_height()
            return new_node, path_len

        if key < node.key:
            inserted_node, path_len = self.__rec_insert__(key, val, node.left, path_len + 1)
            node.left = inserted_node
            inserted_node.parent = node
        else:
            inserted_node, path_len = self.__rec_insert__(key, val, node.right, path_len + 1)
            node.right = inserted_node
            inserted_node.parent = node
        node.update_height()
        return self.__rebalance__(node), path_len
 

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
        if left_child.right.is_real_node():
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
        if right_child.left.is_real_node():
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
        return None


    """returns the node with the maximal key in the dictionary

    @rtype: AVLNode
    @returns: the maximal node, None if the dictionary is empty
    """
    def max_node(self):
        return self.max_node

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """
    def size(self):
        return self.size	


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """
    def get_root(self):
        return self.root
