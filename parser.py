# List representation of the grammar
# 1 + 2 * 3
# [1, +, [2, *, 3]]


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.token = self.tokens[self.idx]

    def factor(self):
        token = self.token
        # Number
        if token.type == "INT" or token.type == "FLOAT":
            return self.token
        # Parentheses
        elif token.value == "(":
            self.advance()
            expression = self.boolean_expr()
            return expression
        # Variable
        elif token.type.startswith("VAR"):
            return self.token
        # Not operator
        elif token.value == "not":
            operator = self.token
            self.advance()
            operand = self.boolean_expr()

            return [operator, operand]
        # Unary operators
        elif self.token.value == "+" or self.token.value == "-":
            operator = self.token
            self.advance()
            operand = self.boolean_expr()

            return [operator, operand]

    # e.g. 2 * 3 -> [2, *, 3]
    def term(self):
        left_node = self.factor()
        self.advance()
        while self.token.value in ["*", "/"]:
            operation = self.token
            self.advance()
            right_node = self.factor()
            self.advance()
            left_node = [left_node, operation, right_node]

        return left_node

    def expr(self):
        left_node = self.term()
        while self.token.value in ["+", "-"]:
            operation = self.token
            self.advance()
            right_node = self.term()
            left_node = [left_node, operation, right_node]

        return left_node

    def statement(self):
        if self.token.type == "DECL":
            # Variable Assignment
            self.advance()
            left_node = self.variable()
            self.advance()
            if self.token.value == "=":
                operation = self.token
                self.advance()
                right_node = self.boolean_expr()
                return [left_node, operation, right_node]

        elif (
            self.token.type == "INT"
            or self.token.type == "FLOAT"
            or self.token.type == "OPT"
            or self.token.value == "not"
        ):
            # Arithmetic Expression
            return self.boolean_expr()

        elif self.token.value == "if":
            return [self.token, self.if_statements()]
        elif self.token.value == "while":
            return [self.token, self.while_statement()]

    def variable(self):
        if self.token.type.startswith("VAR"):
            return self.token

    def comp_expr(self):
        left_node = self.expr()
        while self.token.type == "COMP":
            operator = self.token
            self.advance()
            right_node = self.expr()
            left_node = [left_node, operator, right_node]

        return left_node

    def boolean_expr(self):
        left_node = self.comp_expr()
        while self.token.value == "and" or self.token.value == "or":
            operator = self.token
            self.advance()
            right_node = self.comp_expr()
            left_node = [left_node, operator, right_node]

        return left_node

    def if_statement(self):
        self.advance()
        condition = self.boolean_expr()

        if self.token.value == "do":
            self.advance()
            action = self.statement()
            return [condition, action]
        elif self.tokens[self.idx - 1].value == "do":
            action = self.statement()
            return [condition, action]

    def if_statements(self):
        conditions = []
        actions = []
        if_statement = self.if_statement()

        conditions.append(if_statement[0])
        actions.append(if_statement[1])

        while self.token.value == "elif":
            if_statement = self.if_statements()
            conditions.append(if_statement[0])
            actions.append(if_statement[1])

        if self.token.value == "else":
            self.advance()
            self.advance()
            else_action = self.statement()

            return [conditions, actions, else_action]

        return [conditions, actions]

    def while_statement(self):
        self.advance()
        condition = self.boolean_expr()

        if self.token.value == "do":
            self.advance()
            action = self.statement()
            return [condition, action]

        elif self.tokens[self.idx - 1].value == "do":
            action = self.statement()
            return [condition, action]

    def parse(self):
        return self.statement()

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]
