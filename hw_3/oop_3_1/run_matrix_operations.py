from matrix import Matrix
import numpy as np


def test_operations():
    np.random.seed(0)
    matrix_1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix_2 = Matrix(np.random.randint(0, 10, (10, 10)))

    add_result = matrix_1 + matrix_2
    mul_result = matrix_1 * matrix_2
    matmul_result = matrix_1 @ matrix_2

    add_result.to_file("matrix+")
    mul_result.to_file("matrix*")
    matmul_result.to_file("matrix@")


if __name__ == "__main__":
    test_operations()
