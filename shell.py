from lexer import Lexer
from parser import Parser

while True:
    try:
        text = input("ShadowScript> ")

        lexer = Lexer(text)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        tree = parser.parse()

        print(tokens)
        print(tree)
        
    except Exception as e:
        print(f"An error occurred: {e}")
