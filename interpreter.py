# Interpreter is responsible for interpreting the AST and executing the code.

from tokens import Float, Integer, Reserved


class Interpreter:
    def __init__(self, tree, base):
        self.tree = tree
        self.data = base

    def visit_INT(self, value):
        return int(value)

    def visit_FLOAT(self, value):
        return float(value)

    def visit_VAR(self, id):
        variable = self.data.read(id)
        variable_type = str(variable.type)

        return getattr(self, f"visit_{variable_type}")(variable.value)

    def compute_bin(self, left, operator, right):
        left_type = "VAR" if str(left.type).startswith("VAR") else str(left.type)
        right_type = "VAR" if str(right.type).startswith("VAR") else str(right.type)

        if operator.value == "=":
            left.type = f"VAR({right_type})"
            self.data.write(left, right)
            return self.data.read_all()

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
        elif operator.value == ">":
            output = 1 if left > right else 0
        elif operator.value == "<":
            output = 1 if left < right else 0
        elif operator.value == ">=":
            output = 1 if left >= right else 0
        elif operator.value == "<=":
            output = 1 if left <= right else 0
        elif operator.value == "?=":
            output = 1 if left == right else 0
        elif operator.value == "<>":
            output = 1 if left != right else 0
        elif operator.value == "and":
            output = 1 if left and right else 0
        elif operator.value == "or":
            output = 1 if left or right else 0

        return (
            Integer(output)
            if (left_type == "INT" and right_type == "INT")
            else Float(output)
        )

    def compute_unary(self, operator, operand):
        operand_type = (
            "VAR" if str(operand.type).startswith("VAR") else str(operand.type)
        )
        operand = getattr(self, f"visit_{operand_type}")(operand.value)

        if operator.value == "+":
            output = +operand
        elif operator.value == "-":
            output = -operand
        elif operator.value == "not":
            output = 1 if not operand else 0

        return Integer(output) if (operand_type == "INT") else Float(output)

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree

        # Conditional
        if isinstance(tree, list):
            if isinstance(tree[0], Reserved):
                if tree[0].value == "if":
                    for idx, condition in enumerate(tree[1][0]):
                        evaluation = self.interpret(condition)
                        if evaluation.value == 1:
                            return self.interpret(tree[1][1][idx])
                        else:
                            return 0
                    if len(tree[1]) == 3:
                        return self.interpret(tree[1][2])
                    else:
                        return False
                elif tree[0].value == "while":
                    condition = self.interpret(tree[1][0])
                    while condition.value == 1:
                        # Action
                        print(self.interpret(tree[1][1]))
                        # Condition
                        condition = self.interpret(tree[1][0])
                    return

        # Unary operation
        if isinstance(tree, list) and len(tree) == 2:
            expression = tree[1]
            if isinstance(expression, list):
                expression = self.interpret(expression)
            return self.compute_unary(tree[0], expression)

        # No Operation
        elif not isinstance(tree, list):
            return tree

        # Binary operation
        else:
            # Post-order traversal - Left, Right, Root
            # Evaluating left subtree
            left_node = tree[0]
            if isinstance(left_node, list):
                left_node = self.interpret(left_node)

            # Evaluating right subtree
            right_node = tree[2]
            if isinstance(right_node, list):
                right_node = self.interpret(right_node)

            operator = tree[1]  # Root node

            return self.compute_bin(left_node, operator, right_node)
