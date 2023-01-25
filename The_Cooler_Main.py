import z3
import operator

equation_ = input('Input Equation: ').split(' ')
decipherer = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
    '^': operator.pow,
    '_': lambda root, num: root ** (num / 100),
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
}
decipherer_2 = ['=', '!=', '<', '>', '<=', '>=']
"""
6*(1+2)
"""


def parse_equation(equation):
    parsed_equation = []
    is_simplify_only = True
    for part in equation:
        if part in ('(', ')'):
            parsed_equation.append((part, f'{"l" if part == "(" else "r"}_bracket'))
        elif part in decipherer:
            parsed_equation.append((part, 'op'))
            if part in decipherer_2:
                is_simplify_only = False
        else:
            try:
                part = int(part)
                parsed_equation.append((part, 'int'))
            except ValueError:
                parsed_equation.append((part, 'var'))
    return parsed_equation, is_simplify_only


def order_of_ops(parsed_equation):
    operations_in_order = []
    for index, part in enumerate(parsed_equation):
        if part[1] == 'l_bracket':
            current_index = index
            inbetween = []
            ignores = 0
            while True:
                current_index += 1
                try:
                    if parsed_equation[current_index][1] == 'l_bracket':
                        ignores += 1
                    if parsed_equation[current_index][1] == 'r_bracket':
                        if ignores <= 0:
                            break
                        else:
                            ignores -= 1
                    else:
                        inbetween.append(parsed_equation[current_index])
                except:
                    return 'Invalid_Equation'
            operations_in_order.append((inbetween, 'B'))
        if part[1] == '':
            pass


print(parse_equation(equation_))
