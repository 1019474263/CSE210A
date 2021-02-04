import sys
from lark import Lark

state = {}

calc_grammar = """
    ?start: aexp
        | bexp
        | c

    ?aexp: atom                 -> atom
        | aexp "+" aexp         -> add
        | aexp "-" aexp         -> sub
        | aexp "*" aexp         -> mul
        | aexp "/" aexp         -> div
        | "-" aexp              -> neg
        | "(" aexp ")"          -> apar

    ?bexp: "true"               -> true
        | "false"               -> false
        | aexp "=" aexp         -> equal
        | aexp "<" aexp         -> leq
        | bexp "∧" bexp         -> and_op
        | bexp "∨" bexp         -> or_op
        | "¬" bool_block        -> not_op
        | "(" bexp ")"          -> bpar

    ?bool_block: "true"         -> true
        | "false"               -> false
        | aexp "=" aexp         -> equal
        | aexp "<" aexp         -> leq
        | "(" bexp ")"          -> bpar

    ?c: NAME ":=" exp           -> assign_var
        | c ";" c               -> sequence
        | "if" bexp "then" codeblock "else" codeblock -> if_op
        | "while" bexp "do" codeblock   -> while_op
        | "{" c "}"             -> bracket
        | "skip"                -> skip_op

    ?codeblock: NAME ":=" exp   -> assign_var
        | "if" bexp "then" c "else" c  -> if_op
        | "while" bexp "do" codeblock  -> while_op
        | "{" c "}"             -> bracket
        | "skip"                -> skip_op

    ?exp: aexp                  
        | bexp

    ?atom: NUMBER
        | NAME

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE
    %import common.NEWLINE
    %ignore NEWLINE
    %ignore WS_INLINE
"""

calc_parser = Lark(calc_grammar, lexer='standard', parser='lalr')
calc = calc_parser.parse


def aexp(tree):
    if tree.data == 'atom':
        return atom(tree.children[0])
    elif tree.data == 'add':
        return aexp(tree.children[0]) + aexp(tree.children[1])
    elif tree.data == 'sub':
        return aexp(tree.children[0]) - aexp(tree.children[1])
    elif tree.data == 'mul':
        return aexp(tree.children[0]) * aexp(tree.children[1])
    elif tree.data == 'div':
        try:
            return aexp(tree.children[0]) / aexp(tree.children[1])
        except ZeroDivisionError:
            print("Error: can not divide by zero!")
    elif tree.data == 'neg':
        return - aexp(tree.children[0])
    elif tree.data == 'apar':
        return aexp(tree.children[0])

def show_aexp(tree):
    if tree.data == 'atom':
        return show_atom(tree.children[0])
    elif tree.data == 'add':
        return "(" + show_aexp(tree.children[0]) + "+" + show_aexp(tree.children[1])
    elif tree.data == 'sub':
        return "(" + show_aexp(tree.children[0]) + "-" + show_aexp(tree.children[1])
    elif tree.data == 'mul':
        return "(" + show_aexp(tree.children[0]) + "*" + show_aexp(tree.children[1])


def show_atom(token):
    return token.value

def atom(token):
    if token.type == 'NUMBER':
        return int(token.value)
    else:
        if token.value not in state:
            # state[token.value] = 0
            return 0
        else:
            return state[token.value]


def assign_var(name, tree):
    state[name] = aexp(tree)

def show_assign(var, value):


def bexp(tree):
    if tree.data == 'true':
        return True
    elif tree.data == 'false':
        return False
    elif tree.data == 'equal':
        return aexp(tree.children[0]) == aexp(tree.children[1])
    elif tree.data == 'leq':
        return aexp(tree.children[0]) < aexp(tree.children[1])
    elif tree.data == 'not_op':
        return not bexp(tree.children[0])
    elif tree.data == 'and_op':
        return bexp(tree.children[0]) and bexp(tree.children[1])
    elif tree.data == 'or_op':
        return bexp(tree.children[0]) or bexp(tree.children[1])
    elif tree.data == 'bpar':
        return bexp(tree.children[0])


def if_op(condition, exp1, exp2):
    if bexp(condition):
        eval(exp1)
    else:
        eval(exp2)


def while_op(condition, exp):
    while bexp(condition):
        eval(exp)


def bracket(commands):
    for each in commands:
        eval(each)


def eval(tree):
    if tree.data == 'assign_var':
        assign_var(tree.children[0].value, tree.children[1])
    elif tree.data == 'skip':
        pass
    elif tree.data == 'sequence':
        eval(tree.children[0])
        eval(tree.children[1])
    elif tree.data == 'if_op':
        if_op(tree.children[0], tree.children[1], tree.children[2])
    elif tree.data == 'while_op':
        while_op(tree.children[0], tree.children[1])
    elif tree.data == 'bracket':
        bracket(tree.children)
    elif tree.data == 'skip_op':
        pass
    else:
        raise KeyError()





def show(tree):
    if tree.data == 'assign_var':
        show_assign(tree.children[0].value, tree.children[1])

def main():
    # for line in sys.stdin:
    #     tree = calc(line)
    #     eval(tree)
    #     keys = state.keys()
    #     keys = sorted(keys)
    #     output = ""
    #     for each in keys:
    #         output += f"{each} → {state[each]}, "
    #     if len(output) > 0:
    #         print(f"{{{output[:-2]}}}")
    #     else:
    #         print("{}")
    tree = calc("x:= 1\n")
    print(tree)
    # for each in tree.iter_subtrees_topdown():
    #     print(each)
    eval(tree)
    show(tree)
    print(state)


if __name__ == '__main__':
    main()
