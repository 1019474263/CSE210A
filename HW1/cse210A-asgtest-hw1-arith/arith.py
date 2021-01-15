import sys


def parser(expr):
    length = len(expr)
    elements = expr.split()
    if length < 3:
        print("Error: cannot parser the statement")
    else:
        return statement_parser(elements)


def statement_parser(elements):
    operator = {'+', '-', '*', '/', '**'}
    try:
        if len(elements) == 0:
            return []
        elif len(elements) == 1:
            return elements[0]
        elif elements[1] in operator:
            if len(elements) < 3:
                raise SyntaxError(f"Missing values for {elements[1]}")
            # check if the preceding or succeeding element are valid numbers
            if invalid_number(elements[0]) or invalid_number(elements[2]):
                raise SyntaxError(f"Invalid syntax: {elements[0]} {elements[1]} {elements[2]}")
            if elements[1] in {'+', '-'}:  # [1, +, []]
                return [elements[0], elements[1], statement_parser(elements[2:])]
            elif elements[1] in {'*', '/'}:  # [[1, *, 2], ...]
                # check if a exp is followed
                if 4 <= len(elements) and elements[3] == '**':
                    # check if there are enough terms
                    if len(elements) < 5:
                        raise SyntaxError(f"Invalid syntax: missing values {elements[4]}")
                    # check if the value followed is valid
                    if invalid_number(elements[4]):
                        raise SyntaxError(f"Invalid syntax: {' '.join(elements[2: 5])}")
                    exp = [elements[0], elements[1], elements[2:5]]
                    exp.extend(elements[5:])
                    return statement_parser(exp)
                else:
                    product = [elements[0:3]]
                    product.extend(elements[3:])
                    return statement_parser(product)
            elif elements[1] == '**':
                exp = [elements[0:3]]
                exp.extend(elements[3:])
                return statement_parser(exp)
        else:
            raise SyntaxError(f"Invalid syntax: {elements[0]}  {elements[1]}")
    except SyntaxError:
        raise


def invalid_number(element):
    if type(element) == list:
        return False
    operator = {'+', '-'}
    if not element.isnumeric():
        if element[0] in operator and element[1:].isnumeric():
            return False
        else:
            return True
    return False


def is_operator(element):
    operator = {'+', '-', '*', '/', '**'}
    if type(element) == str and element in operator:
        return True
    return False


def eval(ast):
    if type(ast[0]) == str and type(ast[2]) == str:
        return calculate(int(ast[0]), ast[1], int(ast[2]))
    elif type(ast[0]) == str and type(ast[2]) == list:
        return calculate(int(ast[0]), ast[1], eval(ast[2]))
    elif type(ast[0]) == list and type(ast[2]) == str:
        return calculate(eval(ast[0]), ast[1], int(ast[2]))
    elif type(ast[0]) == list and type(ast[2]) == list:
        return calculate(eval(ast[0]), ast[1], eval(ast[2]))
    else:
        raise ValueError(ast)


def calculate(num1, operator, num2):
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2
    elif operator == '**':
        return num1 ** num2
    else:
        raise ValueError(f"Invalid value: {operator}")


def main():
    for line in sys.stdin:
        print(eval(parser(line)))
    # print(parser("2 * 2 ** 2"))


if __name__ == '__main__':
    main()
