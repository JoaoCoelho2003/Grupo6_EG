from lark import Lark

grammar = """
start: function_declaration* "func" "main" "()" "{" statement* return_statement "}"

statement: variable_declaration ";"
    | assignment ";"
    | print_statement ";"
    | function_call ";"
    | loop
    | conditional
    | "break" ";"
    | "continue" ";"

variable_declaration: TYPE VAR "=" expr

assignment_aux: VAR ASS_OP expr
        | VAR "++"
        | VAR "--"
                    
assignment: VAR "=" expr
        | assignment_aux
        
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

loop: for_loop | while_loop

for_loop: "for" "(" variable_declaration ";" for_cond ";" for_update ")" "{" statement* "}" 

for_cond: bool_expr

for_update: assignment_aux

while_loop: "while" "(" bool_expr ")" "{" statement* "}"

conditional: if_statement | switch_statement

if_statement: "if" "(" bool_expr ")" "{" statement* "}" (elif_statement)* (else_statement)?

elif_statement: "elif" "(" bool_expr ")" "{" statement* "}"

else_statement: "else" "{" statement* "}"

switch_statement: "switch" "(" expr ")" "{" case_statement* default_statement? "}"

case_statement: "case" expr ":" statement*

default_statement: "default" ":" statement*

bool_expr: expr LOGICAL_OP expr
    | function_call

TYPE.2: "int" | "double" | "string" | "set" | "array" | "tuplo"
VAR: /[a-z]+(_[a-z]+)*/
NUMBER: /-?\\d+(\\.\\d+)?/
STRING: /".*"/
OP: "+" | "-" | "*" | "/"
LOGICAL_OP: "==" | "!=" | "<=" | ">=" | "<" | ">"
ASS_OP: "+=" | "-=" | "*=" | "/="

%import common.WS
%ignore WS
"""

code = """
func add(int a, int b) {
    return a + b;
}

func main() {
    int i = 0;
    while (i <= 5) {
        print(i);
        i++;
    }
    
    for (int j = 0; j < 3; j++) {
        print(j);
    }
    
    int result = add(3, 4);
    print(result);
    
    int x = 10;
    if (x < 5) {
        print("x is less than 5");
    } elif (x == 10) {
        print("x is 10");
    } else {
        print("x is greater than 5 and not 10");
    }
    
    switch (x) {
        case 5:
            print("x is 5");
            break;
        case 10:
            print("x is 10");
            break;
        default:
            print("x is neither 5 nor 10");
    }
    
    return 0;
}
"""

parser = Lark(grammar, start='start', parser='lalr')

tree = parser.parse(code)

print(tree.pretty())