# "2 + 3" -> Tokens: [1, +, 3]
# INT - Integer
# FLOAT - Float
# STR - String
# CHAR - Character
# BOOL - Boolean
# OPT - Operator
# RO - Relation Operator
# KW - Keyword
# ID - Identifier
# PUNC - Punctuation
# WS - Whitespace
# EOL - End of Line


class Lexer:
    digits = "0123456789"
    operators = "+-*/"
    ws = [" ", "\n", "\t"]

    def __init__(self, text):
        self.text = text  # client string input, e.g. "2 + 3"
        self.idx = 0  # current position in input
        self.tokens = []  # list of tokens
        self.current_char = self.text[self.idx]  # current character in the input
        self.token = None

    def tokenize(self):
        while self.idx < len(self.text):
            # Handle digits
            if self.current_char in Lexer.digits:
                self.token = self.extractNumber()
            # Handle operators
            elif self.current_char in Lexer.operators:
                self.token = self.extractOperator()
            # Handle whitespace
            elif self.current_char in Lexer.ws:
                self.advance()
                continue

            # Append the tokens list
            self.tokens.append(self.token)
        return self.tokens

    # Extract a number from the text e.g. "123" or "123.456"
    def extractNumber(self):
        number = ""
        is_float = False
        while (self.current_char in Lexer.digits or self.current_char == ".") and (
            self.idx < len(self.text)
        ):
            if self.current_char == ".":
                is_float = True
            number += self.current_char
            self.advance()
        return Integer(number) if not is_float else Float(number)

    # Extract an operator from the text
    def extractOperator(self):
        operator = self.current_char
        self.advance()
        return Operator(operator)

    # Advance/Move the 'idx' pointer and set the 'current_char' variable
    def advance(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.current_char = self.text[self.idx]


# Token class to store the token type and value e.g. Token(INT, 3)
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        # return f"{self.type}:{self.value}"
        return f"{self.value}"


class Integer(Token):
    def __init__(self, value):
        super().__init__("INT", value)
        self.value = value

    def __repr__(self):
        return super().__repr__()


class Float(Token):
    def __init__(self, value):
        super().__init__("FLOAT", value)
        self.value = value

    def __repr__(self):
        return super().__repr__()


class Operator(Token):
    def __init__(self, value):
        super().__init__("OPT", value)
        self.value = value

    def __repr__(self):
        return super().__repr__()


# while self.idx < len(self.text):
#     if self.current_char.isspace():
#         self.advance()
#     elif self.current_char.isdigit():
#         self.tokens.append(self.integer())
#     elif self.current_char == "+":
#         self.tokens.append(Token("PLUS", self.current_char))
#         self.advance()
#     else:
#         raise Exception("Invalid character")
# return self.tokens
