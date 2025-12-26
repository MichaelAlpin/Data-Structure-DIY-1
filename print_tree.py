class TreePrinter:
    """
    מחלקת עזר להדפסת מבנה העץ בטרמינל.
    מדפיסה את העץ בצורה אופקית כך שהשורש בצד שמאל.
    """
    @staticmethod
    def print_tree(node, virtual_node, indent="", last=True):
        # בדיקה אם הצומת הוא וירטואלי או None (לפי המימוש ב-AVL.py)
        if node is None or node is virtual_node or not node.is_real_node():
            return

        # הדפסת התת-עץ הימני (יופיע למעלה)
        new_indent = indent + ("    " if last else "│   ")
        TreePrinter.print_tree(node.right, virtual_node, new_indent, False)

        # הדפסת הצומת הנוכחי
        prefix = "└── " if last else "┌── "
        # במקרה של השורש, אין פרפיקס של בן
        if indent == "":
            prefix = "Root: "
            
        print(indent + prefix + str(node.key))

        # הדפסת התת-עץ השמאלי (יופיע למטה)
        TreePrinter.print_tree(node.left, virtual_node, new_indent, True)

# דוגמה לשימוש בתוך ה-Tester שלך:
# printer = TreePrinter()
# printer.print_tree(tree.root, tree.virtual_node)