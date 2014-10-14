from transducers import *

small_array = [0,1,2,3,4,5,6,7,8,9]

inc = lambda n: n+1

is_even = lambda n: (n % 2) == 0

square = lambda n: n*n

keep_even = lambda n: True if (n % 2 == 0) else False

def keep_idx_fn(i, x):
    try:
        return { 
            0: True,
            2: True,
            3: True,
            6: True,
            7: True
        }[i]
    except KeyError:
        return False

less_than_five = lambda x: x < 5

array_clone = lambda a: list(a)

reverse = lambda a: list(reversed(array_clone(a)))

def array_push(a, x):
    a.append(x)
    return a


def test_transduce():
    res = t_transduce(t_map(inc), array_push, [], small_array)
    assert res == map(inc, small_array)


def test_filter():
    res = t_transduce(t_filter(is_even), array_push, [], small_array)
    assert res == filter(is_even, small_array)


def test_remove():
    res = t_transduce(t_remove(is_even), array_push, [], small_array)
    assert res == filter(t_complement(is_even), small_array)


def test_keep():
    res = t_transduce(t_keep(keep_even), array_push, [], small_array)
    assert res == filter(is_even, small_array)


def test_keep_indexed():
    res = t_transduce(t_keep_indexed(keep_idx_fn), array_push, [], small_array)
    assert res == [0,2,3,6,7]


def test_mapcat():
    res = t_transduce(t_mapcat(reverse), array_push, [], [[3,2,1],[6,5,4],[9,8,7]])
    print res
    assert res == [1,2,3,4,5,6,7,8,9]


def test_into():
    xf = t_map(inc)
    res = t_into([], xf, small_array)
    assert res == [1,2,3,4,5,6,7,8,9,10]


test_into()