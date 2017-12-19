from __pypy__ import reversed_dict, move_to_end, objects_in_repr
from _operator import eq as _eq
import _collections_abc


class OrderedDict(dict):
    '''Dictionary that remembers insertion order.

    In PyPy all dicts are ordered anyway.  This is mostly useful as a
    placeholder to mean "this dict must be ordered even on CPython".

    Known difference: iterating over an OrderedDict which is being
    concurrently modified raises RuntimeError in PyPy.  In CPython
    instead we get some behavior that appears reasonable in some
    cases but is nonsensical in other cases.  This is officially
    forbidden by the CPython docs, so we forbid it explicitly for now.
    '''
    def __init__(*args, **kwds):
        '''Initialize an ordered dictionary.  The signature is the same as
        regular dictionaries, but keyword arguments are not recommended because
        their insertion order is arbitrary.

        '''
        if not args:
            raise TypeError("descriptor '__init__' of 'OrderedDict' object "
                            "needs an argument")
        self, *args = args
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        self.__update(*args, **kwds)

    update = __update = _collections_abc.MutableMapping.update

    def __reversed__(self):
        return reversed_dict(self)

    def popitem(self, last=True):
        '''od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.

        '''
        if last:
            return dict.popitem(self)
        else:
            it = dict.__iter__(self)
            try:
                k = next(it)
            except StopIteration:
                raise KeyError('dictionary is empty')
            return (k, self.pop(k))

    def move_to_end(self, key, last=True):
        '''Move an existing element to the end (or beginning if last==False).

        Raises KeyError if the element does not exist.
        When last=True, acts like a fast version of self[key]=self.pop(key).

        '''
        return move_to_end(self, key, last)

    def __repr__(self):
        'od.__repr__() <==> repr(od)'
        if not self:
            return '%s()' % (self.__class__.__name__,)
        currently_in_repr = objects_in_repr()
        if self in currently_in_repr:
            return '...'
        currently_in_repr[self] = 1
        try:
            return '%s(%r)' % (self.__class__.__name__, list(self.items()))
        finally:
            try:
                del currently_in_repr[self]
            except:
                pass

    def __reduce__(self):
        'Return state information for pickling'
        inst_dict = vars(self).copy()
        return self.__class__, (), inst_dict or None, None, iter(self.items())

    def copy(self):
        'od.copy() -> a shallow copy of od'
        return self.__class__(self)

    def __eq__(self, other):
        '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        '''
        if isinstance(other, OrderedDict):
            return dict.__eq__(self, other) and all(map(_eq, self, other))
        return dict.__eq__(self, other)

    __ne__ = object.__ne__

    def keys(self):
        "D.keys() -> a set-like object providing a view on D's keys"
        return _OrderedDictKeysView(self)

    def items(self):
        "D.items() -> a set-like object providing a view on D's items"
        return _OrderedDictItemsView(self)

    def values(self):
        "D.values() -> an object providing a view on D's values"
        return _OrderedDictValuesView(self)


class _OrderedDictKeysView(_collections_abc.KeysView):
    def __reversed__(self):
        yield from reversed_dict(self._mapping)

class _OrderedDictItemsView(_collections_abc.ItemsView):
    def __reversed__(self):
        for key in reversed_dict(self._mapping):
            yield (key, self._mapping[key])

class _OrderedDictValuesView(_collections_abc.ValuesView):
    def __reversed__(self):
        for key in reversed_dict(self._mapping):
            yield self._mapping[key]
