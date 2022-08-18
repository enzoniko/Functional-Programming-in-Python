import random
from Monads import *
from Decorators import *
import urllib.request


def v2(a) -> int:
    return a*2


def div(a, b):
    return a / b


def sums(a, b, c):
    return a + b + c


def sum_comb(a):
    return a**2


def sum_combv2(a, b):
    return a**2 + b**2


def io_and_cpu_expensive_function(x):
    write_count = 500
    with urllib.request.urlopen(addrs[x % 16], timeout=20) as conn:
        page = conn.read()
        for _ in range(write_count):
            with open('output.txt', 'w') as output:
                output.write(str(page))

    l = [sum_comb(i) for i in range(x)]
    return sum(l)


def io_and_cpu_expensive_functionv2(x, y):
    write_count = 500

    for _ in range(write_count):
        with open('output.txt', 'w') as output:
            output.write(str(sum_comb(x + y)))

    return sum_comb(x + y)


addrs = ['http://www.poatek.com',
         'https://www.poatek.com/team/',
         'https://www.poatek.com/blog/',
         'https://www.poatek.com/our-method/',
         'https://www.poatek.com/services/',
         'https://en.wikipedia.org/wiki/Main_Page',
         'https://www.google.com/',
         'https://www.kaggle.com/competitions',
         'https://www.amazon.com/charts/mostread/fiction/',
         'https://www.amazon.com/charts/mostread/nonfiction',
         'https://www.amazon.com/charts/mostsold/nonfiction',
         'https://www.amazon.com/charts/mostsold/fiction',
         'https://www.nytimes.com',
         'https://www.bbc.com/',
         'https://www.lemonde.fr',
         'https://edition.cnn.com',
         ]


if __name__ == '__main__':

    @ debug_result_time_decorator
    def NotParallel(arguments=[], functions=[]):
        return list({arguments[i]: (FailureMonad(arguments[i]).bind(functions[i]).value) % 10 if (FailureMonad(arguments[i]).bind(functions[i]).value) is not None else None for i in range(len(arguments))}.values())

    @ debug_result_time_decorator
    def NotParallelv2(arguments=[], functions=[]):
        return [str(FailureMonad(arguments[i][0]).consecutive_binds(functions[i], arguments[i][1:]).value)[:10] if (FailureMonad(arguments[i][0]).consecutive_binds(functions[i], arguments[i][1:]).value) is not None else FailureMonad(arguments[i][0]).consecutive_binds(functions[i], arguments[i][1:]).error_status for i in range(len(arguments))]

    def NotParallelv3(arguments=[], functions=[]):
        return
    arguments = []
    funcs = [sum_combv2, io_and_cpu_expensive_functionv2]
    functions = []
    for i in range(10):
        ag = []
        fs = []
        for _ in range(10):
            ag.append(random.randint(0, 100000))
            fs.append(funcs[random.randint(0, 1)])
        arguments.append(ag)
        functions.append(fs)
    pool = ParallelFailureMonadsPool(arguments, functions)
    pool.compute(True, True)
    pool.compute(True)

    NotParallelv2(arguments, functions)
