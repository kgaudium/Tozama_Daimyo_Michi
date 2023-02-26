import copy, random


def zeros(shape, value=0):
    res = value

    for i in range(len(shape)):
        res = (res,) * (shape[len(shape) - i - 1])

    return list(map(lambda x: list(x), res))


def random_mtx(x, y, scope=(0, 9)):
    res = zeros((x, y))
    for i in range(len(res)):
        for j in range(len(res[i])):
            res[i][j] = random.randint(*scope)

    return res

def print_mtx(mtx):
    res = ''

    for i in mtx:
        pre = '|'
        for j in i:
            pre += str(j) + ' '

        res += pre[:-1] + '|\n'

    print(res[:-1])


def flip_mtx(mtx):
    res = [0 for _ in range(len(mtx))]
    for i in range(len(mtx)):
        res[i] = mtx[len(mtx) - i - 1]

    return res


def get_mtx_column(mtx, column_id):
    if column_id >= len(mtx[0]):
        raise IndexError

    column = []
    for i in range(len(mtx)):
        column += [mtx[i][column_id]]

    return column


def set_column_to_mtx(mtx, column_id, column):
    if column_id >= len(mtx[0]):
        raise IndexError
    elif len(mtx) != len(column):
        raise IndexError

    mat = copy.deepcopy(mtx)

    for i in range(len(mtx)):
        mat[i][column_id] = column[i]

    return mat

def get_mtx_shapes(mtx):
    return len(mtx), len(mtx[0])


def rotate(mtx, side=0):
    # 0 - по часовой, 1 - против
    shapes = get_mtx_shapes(mtx)
    new = zeros((shapes[1], shapes[0]))

    if side == 0:
        for i in range(len(mtx)):
            new = set_column_to_mtx(new, len(mtx) - 1 - i, mtx[i])

    elif side == 1:
        for i in range(len(mtx)):
            new = set_column_to_mtx(new, i, mtx[i][::-1])

    return new

def rotate_self(mtx, side=0):
    # 0 - по часовой, 1 - против
    shapes = get_mtx_shapes(mtx)
    new = zeros((shapes[1], shapes[0]))

    if side == 0:
        for i in range(len(mtx)):
            new = set_column_to_mtx(new, len(mtx) - 1 - i, mtx[i])

    elif side == 1:
        for i in range(len(mtx)):
            new = set_column_to_mtx(new, i, mtx[i][::-1])

    mtx = new

if __name__ == '__main__':
    a = random_mtx(3, 5)
    print_mtx(a)
    print_mtx(rotate(rotate(a), 1))
    print()
