from AVL import AVLTree, AVLNode

def print_tree_status(tree, action_name):
    print(f"\n--- After {action_name} ---")
    print(f"Size: {tree.size() if callable(tree.size) else tree.size}")
    root = tree.get_root()
    print(f"Root: {root.key if root and root.is_real_node() else 'None'}")
    print(f"Max Node: {tree.max_node().key if tree.max_node() and hasattr(tree.max_node(), 'key') else 'None'}")
    print(f"Array (Inorder): {tree.avl_to_array()}")

def test_avl_tree():
    tree = AVLTree()
    
    print("=== Test 1: Empty Tree Edge Cases ===")
    node, path = tree.search(10)
    print(f"Search in empty tree: {node} (Expected: None)")
    print(f"Size of empty tree: {tree.size() if callable(tree.size) else tree.size} (Expected: 0)")
    
    print("\n=== Test 2: Basic Insertions & Balancing ===")
    # הכנסה בסדר שיגרום לסיבובים (למשל סדר עולה)
    keys = [10, 20, 30, 5, 3]
    for k in keys:
        print(f"Inserting key {k}...")
        tree.insert(k, f"val_{k}")
    
    print_tree_status(tree, "Insertions [10, 20, 30, 5, 3]")

    print("\n=== Test 3: Search Functionality ===")
    found_node, path_len = tree.search(20)
    print(f"Search 20: Found {found_node.key if found_node else 'None'}, Path length: {path_len}")
    found_node, path_len = tree.search(999)
    print(f"Search 999 (Missing): Found {found_node}, Path length: {path_len}")

    print("\n=== Test 4: Internal Node Properties ===")
    root = tree.get_root()
    if root:
        print(f"Root Key: {root.key}, Height: {root.height}")
        print(f"Left Child: {root.left.key if root.left.is_real_node() else 'Virtual'}")
        print(f"Right Child: {root.right.key if root.right.is_real_node() else 'Virtual'}")
        print(f"Balance Factor: {root.balance_factor()}")

    print("\n=== Test 5: Unimplemented Functions (Placeholders) ===")
    # פונקציות אלו אמורות להחזיר None או ערכי ברירת מחדל לפי המימוש הנוכחי שלך
    print(f"Finger Search (10): {tree.finger_search(10)}")
    print(f"Finger Insert (40): {tree.finger_insert(40, 'val')}")
    print(f"Delete: {tree.delete(None)}")
    print(f"Join: {tree.join(None, 50, 'val')}")
    print(f"Split: {tree.split(None)}")

    print("\n=== Test 6: Verifying Max Node ===")
    # נוודא ש-max_node מתעדכן נכון
    tree.insert(100, "max")
    print(f"Max node after inserting 100: {tree.max_node().key if hasattr(tree.max_node(), 'key') else 'N/A'}")

    print("\n=== Summary Table ===")
    res = tree.avl_to_array()
    print("Final Tree Structure (Key, Value):")
    for node_obj, val in res:
        print(f"  - Key: {node_obj.key}, Height: {node_obj.height}, Parent: {node_obj.parent.key if node_obj.parent else 'None'}")

if __name__ == "__main__":
    try:
        test_avl_tree()
        print("\n[SUCCESS] Tester finished running.")
    except Exception as e:
        print(f"\n[ERROR] Tester failed with: {e}")
        import traceback
        traceback.print_exc()