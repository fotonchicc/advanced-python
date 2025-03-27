import numpy as np


class ArithmeticMixin:
    def _check_type(self, other):
        if not isinstance(other, self.__class__):
            raise ArithmeticError(f"Right operand must be of type {self.__class__.__name__}")

    def __add__(self, other):
        self._check_type(other)
        return self.__class__(np.add(self.data, other.data))

    def __sub__(self, other):
        self._check_type(other)
        return self.__class__(np.subtract(self.data, other.data))

    def __mul__(self, other):
        self._check_type(other)
        return self.__class__(np.multiply(self.data, other.data))

    def __matmul__(self, other):
        self._check_type(other)
        return self.__class__(np.matmul(self.data, other.data))

    def __truediv__(self, other, decimals=2):
        self._check_type(other)
        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.divide(self.data, other.data)
            result = np.nan_to_num(
                np.around(result, decimals=decimals),
                nan=0.0,
                posinf=0.0,
                neginf=0.0
            )
        return self.__class__(result)


class FileIOMixin:
    def to_file(self, filename):
        with open(f"../artifacts/{filename}.txt", "w", encoding="utf-8") as file:
            file.write(str(self))


class DisplayMixin:
    def __str__(self):
        if self.data.ndim == 1:
            return " ".join(map(str, self.data))
        elif self.data.ndim == 2:
            max_len = max(len(str(num)) for row in self.data for num in row)
            formatted_data = [
                " ".join(f"{num:>{max_len}}" for num in row)
                for row in self.data
            ]
            return "\n".join(formatted_data)
        else:
            raise ValueError("Unsupported data dimensionality")


class PropertyMixin:
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def rows(self):
        return self.data.shape[0]

    @property
    def cols(self):
        return self.data.shape[1]

    @property
    def shape(self):
        return self.data.shape
