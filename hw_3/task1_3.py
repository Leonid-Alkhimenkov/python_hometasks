import numpy as np
from functools import lru_cache


class MatrixHashMixin:
    def __hash__(self):
        """
        Хеш-функция представляет из себя сумму из общей суммы элементов полученной метрицы
        с суммой первой строки матрицы умноженная на сумму числа строк и столбцов и следующего порядка
        относительно первой суммы
        """
        total_sum = sum(sum(row) for row in self.data)
        first_sum = sum(self.data[0])
        return (
            first_sum * (self.rows + self.cols) * (len(str(total_sum)) + 1) + total_sum
        )

    def __eq__(self, other):
        return self.data == other.data


class Matrix(MatrixHashMixin):
    def __init__(self, data):
        self.data = data.tolist() if isinstance(data, np.ndarray) else data

        if len(self.data) == 0:
            raise ValueError("Input matrix error")

        self.rows = len(self.data)
        self.cols = len(self.data[0])

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Incorrect matrix sizes")

        result = [
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Incorrect matrix sizes")

        result = [
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    @lru_cache(maxsize=None)
    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Incorrect matrix sizes")

        result = [
            tuple(
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            )
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.data])

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            for row in self.data:
                f.write(" ".join(map(str, row)) + "\n")


def find_collision():
    while True:
        A = Matrix(np.random.randint(0, 10, (2, 2)))
        C = Matrix(np.random.randint(0, 10, (2, 2)))

        if hash(A) == hash(C) and A != C:
            B = Matrix(np.random.randint(0, 10, (2, 2)))
            D = Matrix(B.data.copy())

            AB = A @ B
            CD = C @ D

            if AB != CD:
                return A, B, C, D, AB, CD


def main1():
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    matrix_sum = matrix1 + matrix2
    matrix_elementwise = matrix1 * matrix2
    matrix_mul = matrix1 @ matrix2

    matrix_sum.save_to_file("matrix+.txt")
    matrix_elementwise.save_to_file("matrix*.txt")
    matrix_mul.save_to_file("matrix@.txt")


def main3():
    A, B, C, D, AB, CD = find_collision()

    A.save_to_file("A.txt")
    B.save_to_file("B.txt")
    C.save_to_file("C.txt")
    D.save_to_file("D.txt")
    AB.save_to_file("AB.txt")
    CD.save_to_file("CD.txt")

    with open("hash.txt", "w") as f:
        f.write(f"Hash of A: {hash(A)}\n")
        f.write(f"Hash of C: {hash(C)}\n")
        f.write(f"Hash of AB: {hash(AB)}\n")
        f.write(f"Hash of CD: {hash(CD)}\n")


if __name__ == "__main__":
    main1()
    main3()
