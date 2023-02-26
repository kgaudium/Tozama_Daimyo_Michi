# def norm(a):
#     return a / np.sqrt(np.sum(a ** 2))

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def length(a):
    return (dot(a, a)) ** 0.5


def mulS(a, value):
    return a[0] * value, a[1] * value


def normalize(a):
    return mulS(a, 1 / length(a))


def summ(a, b):
    return a[0] + b[0], a[1] + b[1]
