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
        if token.type == "INT" or token.type == "FLOAT":
            return self.token

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

    def parse(self):
        return self.expr()

    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]
