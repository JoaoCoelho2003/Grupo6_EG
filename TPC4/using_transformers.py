import sys
from lark import Lark, Transformer

grammar = """
    start: "(" elements ")"
    elements: element ("," element)*
    element: "inicio" -> inicio
           | "fim" -> fim
           | NUMBER -> number
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

class SumTransformer(Transformer):
    def __init__(self):
        self.summing = False
        self.total = 0

    def inicio(self, _):
        self.summing = True

    def fim(self, _):
        self.summing = False

    def number(self, n):
        if self.summing:
            self.total += int(n[0])

def calculate_sum(input_string):
    parser = Lark(grammar, start='start', parser='lalr')
    tree = parser.parse(input_string)
    transformer = SumTransformer()
    transformer.transform(tree)
    return transformer.total

def main():
    if len(sys.argv) > 1:
        input_string = sys.argv[1]
        print(calculate_sum(input_string))
    else:
        while True:
            input_string = input("Enter the string (or 'q' to quit): ")
            if input_string.lower() == 'q':
                break
            try:
                print(calculate_sum(input_string))
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
