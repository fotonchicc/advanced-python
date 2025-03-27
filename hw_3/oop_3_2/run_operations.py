from advanced_array import AdvancedArray
import numpy as np


def test_operations():
    np.random.seed(0)
    matrix_1 = AdvancedArray(np.random.randint(0, 10, (10, 10)))
    matrix_2 = AdvancedArray(np.random.randint(0, 10, (10, 10)))

    add_result = matrix_1 + matrix_2
    sub_result = matrix_1 - matrix_2
    mul_result = matrix_1 * matrix_2
    matmul_result = matrix_1 @ matrix_2
    div_result = matrix_1 / matrix_2

    add_result.to_file("array+")
    sub_result.to_file("array-")
    mul_result.to_file("array*")
    matmul_result.to_file("array@")
    div_result.to_file("array_div")


if __name__ == "__main__":
    test_operations()
