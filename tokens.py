# Token class to store the token type and value e.g. Token(INT, 3)
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return str(self.value)


class Integer(Token):
    def __init__(self, value):
        super().__init__("INT", value)


class Float(Token):
    def __init__(self, value):
        super().__init__("FLOAT", value)


class Operator(Token):
    def __init__(self, value):
        super().__init__("OPT", value)
