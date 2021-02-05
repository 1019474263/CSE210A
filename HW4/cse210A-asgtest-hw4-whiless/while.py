import sys
from lark import Lark

state = {}
rest_of_tree = None
count = 0
skip_only = False
calc_grammar = """
    ?start: aexp
        | bexp
        | c

    ?aexp: atom                 -> atom
        | aexp "+" aexp         -> add
        | aexp "-" aexp         -> sub
        | aexp "*" aexp         -> mul
        | aexp "/" aexp         -> div
        | "-(" aexp ")"         -> neg
        | "-" atom              -> neg_atom
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
    elif tree.data == 'neg_atom':
        return - atom(tree.children[0])
    elif tree.data == 'apar':
        return aexp(tree.children[0])


def show_aexp(tree):
    if tree.data == 'atom':
        return show_atom(tree.children[0])
    elif tree.data == 'add':
        return "(" + show_aexp(tree.children[0]) + "+" + show_aexp(tree.children[1]) + ")"
    elif tree.data == 'sub':
        return "(" + show_aexp(tree.children[0]) + "-" + show_aexp(tree.children[1]) + ")"
    elif tree.data == 'mul':
        return "(" + show_aexp(tree.children[0]) + "*" + show_aexp(tree.children[1]) + ")"
    elif tree.data == 'neg':
        return "-" + show_aexp(tree.children[0])
    elif tree.data == 'neg_atom':
        return "-" + show_atom(tree.children[0])
    elif tree.data == 'apar':
        return show_aexp(tree.children[0])


def show_atom(token):
    if token.value.isnumeric():
        return str(int(token.value))
    else:
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
    return var + " := " + show_aexp(value)


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


def show_bexp(tree):
    if tree.data == 'true':
        return "true"
    elif tree.data == 'false':
        return 'false'
    elif tree.data == 'equal':
        return "(" + show_aexp(tree.children[0]) + "=" + show_aexp(tree.children[1]) + ")"
    elif tree.data == 'leq':
        return "(" + show_aexp(tree.children[0]) + "<" + show_aexp(tree.children[1]) + ")"
    elif tree.data == 'not_op':
        return "¬" + show_bexp(tree.children[0])
    elif tree.data == 'and_op':
        return "(" + show_bexp(tree.children[0]) + "∧" + show_bexp(tree.children[1]) + ")"
    elif tree.data == 'or_op':
        return "(" + show_bexp(tree.children[0]) + "∨" + show_bexp(tree.children[1]) + ")"
    elif tree.data == 'bpar':
        return show_bexp(tree.children[0])


def if_op(condition, exp1, exp2):
    if bexp(condition):
        print_show(show(exp1))
        eval(exp1)
    else:
        print_show(show(exp2))
        eval(exp2)


def show_if(condition, exp1, exp2):
    return "if " + show_bexp(condition) + " then { " + show(exp1) + " } else { " + show(exp2) + " }"


def while_op(condition, exp):

    while bexp(condition):
        print_show(f"{show(exp)}; {show_while(condition, exp)}")
        eval(exp)
        print_show(f"skip; {show_while(condition, exp)}")
        print_show(f"{show_while(condition, exp)}")



def show_while(condition, exp):
    return "while " + show_bexp(condition) + " do { " + show(exp) + " }"


def bracket(commands):
    for each in commands:
        eval(each)

def show_bracket(commands):
    output = ""
    for each in commands:
        output += show(each) + "; "
    if len(output):
        return output[:-2]
    return output


def eval(tree):
    global skip_only
    if tree.data == 'assign_var':
        assign_var(tree.children[0].value, tree.children[1])
    elif tree.data == 'sequence':
        if tree.children[1].data == 'assign_var' and tree.children[0].data == 'bracket':
            seq = tree.children[0].children[0]
            tree.children[0] = seq.children[0]
            seq.children[0] = seq.children[1]
            seq.children[1] = tree.children[1]
            tree.children[1] = seq
            eval(tree)
        else:
            eval(tree.children[0])
            print_show(f"skip; {show(tree.children[1])}")
            print_show(show(tree.children[1]))
            eval(tree.children[1])
    elif tree.data == 'if_op':
        if_op(tree.children[0], tree.children[1], tree.children[2])
    elif tree.data == 'while_op':
        while_op(tree.children[0], tree.children[1])
    elif tree.data == 'bracket':
        bracket(tree.children)
    elif tree.data == 'skip_op':
        if count == 0:
            print("")
            skip_only = True
        pass
    else:
        raise KeyError()


def show(tree):
    if tree.data == 'assign_var':
        return show_assign(tree.children[0].value, tree.children[1])
    elif tree.data == 'sequence':
        return show(tree.children[0]) + "; " + show(tree.children[1])
    elif tree.data == 'if_op':
        return show_if(tree.children[0], tree.children[1], tree.children[2])
    elif tree.data == 'while_op':
        return show_while(tree.children[0], tree.children[1])
    elif tree.data == 'bracket':
        return show_bracket(tree.children)
    elif tree.data == 'skip_op':
        return ""
    else:
        raise KeyError()


def print_show(code):
    global count
    count += 1
    print(f"⇒ {code}, {{{get_state()}}}")
    if count > 9999:
        quit()


def get_state():
    output = ""
    keys = state.keys()
    keys = sorted(keys)
    for each in keys:
        output += f"{each} → {state[each]}, "
    if len(output):
        output = output[:-2]
    return output


def main():
    # for line in sys.stdin:
    #     tree = calc(line)
    #     eval(tree)
    # if not skip_only:
    #     print_show("skip")
    tree = calc(" k := ( 49 ) * 3 + k\n")
    print(tree)
    eval(tree)
    print("⇒ " + show(tree) + ", ")
    print(state)


if __name__ == '__main__':
    main()
