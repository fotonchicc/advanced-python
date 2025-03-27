from matrix import Matrix
import numpy as np


def create_artifacts(A, B, C, D, AB, CD):
    for name, matrix in [('A', A), ('B', B), ('C', C), ('D', D), ('AB', AB), ('CD', CD)]:
        matrix.to_file(name)

    with open(f"../artifacts/hash.txt", "w", encoding="utf-8") as file:
        file.write(f"Hash AB: {hash(AB)}\nHash CD: {hash(CD)}")


def find_collisions():
    np.random.seed(0)
    while True:
        A = Matrix(np.random.randint(0, 5, (5, 5)))
        C = Matrix(np.random.randint(0, 5, (5, 5)))

        if hash(A) == hash(C) and A != C:
            B = Matrix(np.random.randint(0, 5, (5, 5)))
            D = Matrix(B.data.copy())

            AB = A @ B
            Matrix.clear_cache()
            CD = C @ D

            if AB != CD:
                return A, B, C, D, AB, CD


if __name__ == "__main__":
    collision_data = find_collisions()
    create_artifacts(*collision_data)
