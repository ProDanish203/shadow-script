from lexer import Lexer

while True:
    try:
        text = input("ShadowScript> ")

        lexer = Lexer(text)
        tokens = lexer.tokenize()

        print(tokens)
    except Exception as e:
        print(f"An error occurred: {e}")
