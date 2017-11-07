C_GRAD = [31, 91, 33, 93, 32, 92]

# Utility
def map_2d(f, a):
    return [[f(c) for c in r] for r in a]

def zipwith(f, a, b):
    return [f(ac, bc) for ac, bc in zip(a, b)]

def zipwith_2d(f, a, b):
    return [zipwith(f, ar, br) for ar, br in zip(a, b)]

def color(code, s):
    return '\033[{}m{}\033[00m'.format(code, s)

def print_2d_floats(a):
    rowline = '\n+{}\n'.format(('-' * 5 + '+') * len(a[0]))
    print(rowline + rowline.join(
        '|{}|'.format('|'.join(
            color(C_GRAD[min(len(C_GRAD) - 1, int(c * 2 * len(C_GRAD)))],
                  '{:1.0f}'.format(c)) for c in r
        ))
    for r in a) + rowline)
