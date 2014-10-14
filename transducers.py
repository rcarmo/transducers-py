from types import *
from functools import partial

class Transducer:
    def __init__(self, f, xf):
        self.f = f
        self.xf = xf

    def init(self):
        return self.xf.init()

    def result(self, result):
        return self.xf.result(result)

    def step(self):
        pass


class Wrap(Transducer):
    def __init__(self, f):
       self.f = f

    def init(self):
        raise RuntimeError

    def result(self, result):
        return result

    def step(self, result, in_val):
        return self.f(result, in_val)

def t_slice(array_like, start, n = None):
    if n is None:
        return array_like[start:]
    return array_like[start:n]

def t_complement(f):
    return lambda *args: partial(f,t_slice(args,0))


def t_wrap(f):
    return Wrap(f)


class Reduced(Transducer):
    def __init__(self, value):
        self.value = value

def t_reduced(x):
    return Reduced(x)

def t_is_reduced(x):
    return isinstance(x, Reduced)

def t_ensure_reduced(x):
    if t_is_reduced(x):
        return x
    else:
        return t_reduced(x)

def t_unreduced(x):
    if t_is_reduced(x):
        return x.value
    else:
        return x

def t_identity(x):
    return x


def t_comp(*args):
    arglen = len(args)
    if (arglen == 2):
        f = args[0]
        g = args[1]
        return lambda *args: f(g(t_slice(args,0)))

    elif arglen > 2:
        return t_reduce(t_comp, args[0], t_slice(args,1))

    else:
        raise RuntimeError("comp must be given at least 2 arguments")


class Map(Transducer):
    def __init__(self, f, xf):
        self.f = f
        self.xf = xf

    def step(self, result, in_val):
        return self.xf.step(result, self.f(in_val))


def t_map(f):
    return lambda xf: Map(f, xf)


class Filter(Transducer):
    def __init__(self, pred, xf):
        self.pred = pred
        self.xf =xf

    def step(self, result, in_val):
        if(self.pred(in_val)):
            return self.xf.step(result, in_val)
        else:
            return result


def t_filter(pred):
    return lambda xf: Filter(pred, xf)

def t_remove(f):
    return t_filter(t_complement(f))


class Take(Transducer):
    def __init__(self, n, xf):
        self.n = n
        self.xf = xf

    def step(self, result, in_val):
        if(self.n > 0):
            result = self.xf.step(result, in_val)
        else:
            result = ensure_reduced(result)
        self.n -= 1
        return result

def t_take(n):
    return lambda xf: Take(n, xf)


class TakeWhile(Transducer):
    def __init__(self, pred, xf):
        self.pred = pred
        self.xf = xf

    def step(self, result, in_val):
        if self.pred(in_val):
            return self.xf.step(result, in_val)
        else:
            return t_reduced(result)


def t_take_while(pred):
    return lambda xf: TakeWhile(pred, xf)


class TakeNth(Transducer):
    def __init__(self, n, xf):
        self.i = -1
        self.n = n
        self.xf = xf


    def step(self, result, in_val):
        self.i += 1
        if(0 == (self.i % self.n)):
            return self.xf.step(result, in_val)
        return result


def t_take_nth(n):
    return lambda xf: TakeNth(n, xf)


class Drop(Transducer):
    def __init__(self, n, xf):
        self.n = n
        self.xf = xf

    def step(self, result, in_val):
        if self.n > 0:
            self.n -= 1
            return result
        return self.xf.step(result, in_val)


def t_drop(n):
    return lambda xf: Drop(n, xf)


class DropWhile(Transducer):
    def __init__(self, pred, xf):
        self.drop = True
        self.f = pred
        self.xf = xf

    def step(self, result, in_val):
        if self.drop and self.f(in_val):
            return result
        if self.drop:
            self.drop = False
        return self.xf.step(result, in_val)

def t_drop_while(pred):
    return lambda xf: DropWhile(pred, xf)


class PartitionBy(Transducer):
    def __init__(self, f, xf):
        self.f = f
        self.xf = xf
        self.a = []
        self.pval = None

    def result(self, result):
        if len(self.a):
            result = self.xf.step(result, self.a)
            self.a = []
        return self.xf.result(result)

    def step(self, result, in_val):
        pval = self.pval
        val = self.f(in_val)

        self.pval = val
        if (pval == None) or (pval == val):
            self.a.append(in_val)
            return result
        else:
            ret = t_unreduced(self.xf.step(result, self.a))
            self.a = []
            if not(t_is_reduced(ret)):
                self.a.append(in_val)
            return ret


def t_partition_by(f):
    return lambda xf: PartitionBy(f, xf)


class PartitionAll(Transducer):
    def __init__(self, n, xf):
        self.n = n
        self.xf = xf
        self.a = []

    def result(self, result):
        if len(self.a):
            result = self.xf.step(result, self.a)
            self.a = []
        return self.xf.result(result)

    def step(self, result, in_val):
        self.a.append(in_val)
        if (self.n == len(self.a)):
            a = self.a
            self.a = []
            return t_unreduced(self.xf.step(result, a))
        return result

def t_partition_all(n):
    return lambda xf: PartitionAll(n, xf)


class Keep(Transducer):
    def __init__(self, f, xf):
        self.f = f
        self.xf = xf

    def step(self, result, in_val):
        v = self.f(in_val)
        if not v:
            return result
        return self.xf.step(result,in_val)


def t_keep(f):
    return lambda xf: Keep(f, xf)


class KeepIndexed(Transducer):
    def __init__(self, f, xf):
        self.i = -1
        self.f = f
        self.xf = xf

    def step(self, result, in_val):
        self.i += 1
        v = self.f(self.i, in_val)
        if not v:
            return result
        return self.xf.step(result, in_val)

def t_keep_indexed(f):
    return lambda xf: KeepIndexed(f, xf)


class PreservingReduced(Transducer):
    def __init__(self, xf):
        self.xf = xf

    def step(self, result, in_val):
        ret = self.xf.step(result, in_val)
        if t_is_reduced(ret):
            return t_reduced(ret)
        return ret


def t_preserving_reduced(xf):
    return PreservingReduced(xf)


class Cat(Transducer):
    def __init__(self, xf):
        self.xf = xf

    def step(self, result, in_val):
        return t_reduce(t_preserving_reduced(self.xf), result, in_val)


def t_cat(xf):
    return Cat(xf)


def t_mapcat(f):
    return t_comp(t_map(f), t_cat)


def t_iterable_reduce(xf, init, iterable):
    acc = init
    for step in iterable:
        acc = xf.step(acc, step)
        if t_is_reduced(acc):
            acc = acc.value
            break
    return xf.result(acc)


def t_reduce(xf, init, coll):
    if type(xf) == FunctionType:
        xf = t_wrap(xf)
    return t_iterable_reduce(xf, init, coll)


def t_transduce(xf, f, init, coll):
    if type(f) == FunctionType:
        f = t_wrap(f)
    xf = xf(f)
    return t_reduce(xf, init, coll)


def t_into(empty, xf, coll):
    if type(coll) in [ListType, StringType, TupleType]:
        return t_transduce(xf, lambda x, y: x + y, empty, coll)
    raise RuntimeError("can't handle " + type(coll))


class Completing(Transducer):
    def __init__(self, cf, xf):
        self.cf = cf
        self.xf = xf

    def result(self, result):
        return self.cf(result)

    def step(self, result, step):
        return self.xf.step(result, step)


def t_completing(xf, cf):
    return lambda xf, cf: Completing(cf, xf)


def t_to_fn(fn, builder):
    if type(builder) == FunctionType:
        builder = t_wrap(builder)
    
    rxf = xf(builder)
    return partial(rxf.step, [rxf])


def t_first(xf):
    return t_wrap(lambda result, in_val: t_reduced(in_val))


