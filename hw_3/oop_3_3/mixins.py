from collections import OrderedDict


class HashEqMixin:
    def __hash__(self):
        """
        Хэш-функция: сумма элементов матрицы
        """
        return sum(sum(row) for row in self.data)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.data == other.data


class CacheMixin:
    _mul_cache = OrderedDict()
    _matmul_cache = OrderedDict()
    _max_cache_size = 128

    @classmethod
    def _check_cache(cls, cache, key):
        if key in cache:
            cache.move_to_end(key)
            return cache[key]
        return None

    @classmethod
    def _add_to_cache(cls, cache, key, value):
        if len(cache) >= cls._max_cache_size:
            cache.popitem(last=False)
        cache[key] = value

    @classmethod
    def clear_cache(cls):
        cls._mul_cache.clear()
        cls._matmul_cache.clear()
