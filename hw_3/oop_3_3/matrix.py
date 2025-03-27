import numpy as np
from mixins import HashEqMixin, CacheMixin


class Matrix(HashEqMixin, CacheMixin):
    def __init__(self, data):
        if isinstance(data, np.ndarray):
            if not np.issubdtype(data.dtype, np.number):
                raise TypeError("Matrix elements must be numeric")
            self.data = data.tolist()
        elif isinstance(data, Matrix):
            self.data = [row.copy() for row in data.data]
        elif isinstance(data, (tuple, list)):
            for row in data:
                if not all(isinstance(x, (int, float)) for x in row):
                    raise TypeError("All matrix elements must be numeric")
            self.data = [row.copy() for row in data]
        else:
            raise TypeError(f"Unsupported data type: {type(data)}")

        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    __hash__ = HashEqMixin.__hash__
    __eq__ = HashEqMixin.__eq__

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise ArithmeticError("Right operand must be a Matrix object")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must be the same size for addition operation")
        new_data = [
            [self.data[i][j] + other.data[i][j]
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(new_data)

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            raise ArithmeticError("Right operand must be a Matrix object")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must be the same size for component-by-component multiplication")

        cache_key = hash(self) + hash(other)
        if cached := self._check_cache(self._mul_cache, cache_key):
            return cached

        new_data = [
            [self.data[i][j] * other.data[i][j]
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        result = Matrix(new_data)
        self._add_to_cache(self._mul_cache, cache_key, result)
        return result

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            raise ArithmeticError("Right operand must be a Matrix object")
        if self.cols != other.rows:
            raise ValueError("Number of columns in first matrix must match number of rows in second matrix")

        cache_key = hash(self) + hash(other)
        if cached := self._check_cache(self._matmul_cache, cache_key):
            return cached

        new_data = [
            [sum(a * b for a, b in zip(row, col))
             for col in zip(*other.data)]
            for row in self.data
        ]
        result = Matrix(new_data)
        self._add_to_cache(self._matmul_cache, cache_key, result)
        return result

    def __str__(self):
        max_len = max(len(str(num)) for row in self.data for num in row)
        formatted_data = [
            " ".join(f"{num:>{max_len}}" for num in row)
            for row in self.data
        ]
        return "\n".join(formatted_data)

    def to_file(self, filename: str):
        with open(f"../artifacts/{filename}.txt", "w", encoding="utf-8") as file:
            file.write(str(self))
