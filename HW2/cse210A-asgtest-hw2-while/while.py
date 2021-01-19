import sys
from lark import Lark, Transformer, v_args
    #TODO: fix the boolean expressions
calc_grammar = """
    ?start: aexp
        | bexp
        | c

    ?aexp: atom
        | aexp "+" aexp         -> add
        | aexp "-" aexp         -> sub
        | aexp "*" aexp         -> mul
        | aexp "/" aexp         -> div 
    
    ?bexp: "true"               -> true
        | "false"               -> false
        | aexp "=" aexp
        | aexp "<" aexp         
        | "¬" bexp              -> not
        | bexp "∧" bexp         -> and
        | bexp "∨" bexp

    ?c: NAME "=" aexp          -> assign_var
    ?atom: NUMBER              -> number
        | "-" atom             -> neg
        | NAME                 -> var
        | "(" aexp ")"


    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""


@v_args(inline=True)  # Affects the signatures of the methods
class CalculateTree(Transformer):
    from operator import add, sub, mul, neg
    number = float

    def __init__(self):
        self.vars = {}

    def div(self, exp1, exp2):
        try:
            return exp1 / exp2
        except ZeroDivisionError:
            print("ERROR: Can not divide by 0")



    def assign_var(self, name, value):
        self.vars[name] = value
        return value

    def var(self, name):
        try:
            return self.vars[name]
        except KeyError:
            print("ERROR: Variable not found: %s" % name)

    def true(self):
        return True

    def false(self):
        return False


calc_parser = Lark(calc_grammar, lexer='standard', parser='lalr', transformer=CalculateTree())
calc = calc_parser.parse


def main():
    print(calc("true ∧ false"))


if __name__ == '__main__':
    main()
