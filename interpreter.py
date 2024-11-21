# Interpreter is responsible for interpreting the AST and executing the code.

from tokens import Integer, Float, Operator


class Interpreter:
    def __init__(self, tree):
        self.tree = tree

    def visit_INT(self, value):
        return int(value)

    def visit_FLOAT(self, value):
        return float(value)

    def compute(self, left, operator, right):
        left_type = left.type
        right_type = right.type

        left = getattr(self, f"visit_{left_type}")(left.value)
        right = getattr(self, f"visit_{right_type}")(right.value)

        if operator.value == "+":
            output = left + right
        elif operator.value == "-":
            output = left - right
        elif operator.value == "*":
            output = left * right
        elif operator.value == "/":
            output = left / right

        return Integer(output) if isinstance(output, int) else Float(output)

    # Post-order traversal - Left, Right, Root
    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree

        # Evaluating left subtree
        left_node = tree[0]
        if isinstance(left_node, list):
            left_node = self.interpret(left_node)

        # Evaluating right subtree
        right_node = tree[2]
        if isinstance(right_node, list):
            right_node = self.interpret(right_node)

        operator = tree[1]  # Root node

        return self.compute(left_node, operator, right_node)
