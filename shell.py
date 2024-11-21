from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

while True:
    try:
        text = input("ShadowScript> ")

        lexer = Lexer(text)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        tree = parser.parse()

        interpreter = Interpreter(tree)
        result = interpreter.interpret()

        print(result)

    except Exception as e:
        print(f"An error occurred: {e}")
