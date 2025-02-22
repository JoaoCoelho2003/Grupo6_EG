from lark import Lark

grammar = """
start: function_declaration* "func" "main" "()" "{" statement* return_statement "}"

statement: variable_declaration ";"
    | assignment ";"
    | print_statement ";"
    | function_call ";"
    
variable_declaration: TYPE VAR "=" expr
                    
assignment: VAR "=" expr
    | VAR ASS_OP expr
    | VAR "++"
    | VAR "--"
        
expr: VAR
    | NUMBER
    | STRING
    | function_call
    | expr OP expr
    | expr LOGICAL_OP expr
    
print_statement: "print" "(" VAR ")"
        | "print" "(" NUMBER ")"
        | "print" "(" STRING ")"
        
function_declaration: "func" VAR "(" param_list? ")" "{" statement* return_statement "}"

return_statement: "return" expr ";"

param_list: param "," param_list
    | param

param: TYPE VAR

function_call: VAR "(" arg_list? ")"

arg_list: expr "," arg_list
    | expr

TYPE.2: "int" | "double" | "string" | "set" | "array" | "tuplo"
VAR: /[a-z]+(_[a-z]+)*/
NUMBER: /-?\\d+(\\.\\d+)?/
STRING: /".*"/
OP: "+" | "-" | "*" | "/"
LOGICAL_OP: "==" | "!=" | "<=" | ">="
ASS_OP: "+=" | "-=" | "*=" | "/="

%import common.WS
%ignore WS
"""

parser = Lark(grammar, start='start', parser='lalr')

code = """
func add(int x, int y) {
    int sum = x+y;
    return sum;
}


func main() {
    int x = 10;
    int y = 5;
    int sum = add(x,y);
    print(sum);
    return 0;
}
"""

tree = parser.parse(code)

print(tree.pretty())