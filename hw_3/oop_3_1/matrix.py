import numpy as np


class Matrix:
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
        new_data = [
            [self.data[i][j] * other.data[i][j]
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(new_data)

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            raise ArithmeticError("Right operand must be a Matrix object")
        if self.cols != other.rows:
            raise ValueError("Number of columns in first matrix must match number of rows in second matrix")
        new_data = [
            [sum(a * b for a, b in zip(row, col))
             for col in zip(*other.data)]
            for row in self.data
        ]
        return Matrix(new_data)

    def __str__(self):
        max_len = max(len(str(num)) for row in self.data for num in row)
        formatted_data = [
            " ".join(f"{num:>{max_len}}" for num in row)
            for row in self.data
        ]
        return "\n".join(formatted_data)

    def to_file(self, filename):
        with open(f"../artifacts/{filename}.txt", "w", encoding="utf-8") as file:
            file.write(str(self))
