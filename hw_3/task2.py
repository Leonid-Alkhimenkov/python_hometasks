import numpy as np


class ArithmeticMixin:
    def __add__(self, other):
        return self.__class__(self.data + other.data)

    def __mul__(self, other):
        return self.__class__(self.data * other.data)

    def __matmul__(self, other):
        return self.__class__(self.data @ other.data)


class SaveFileMixin:
    def save_to_file(self, filename):
        with open(filename, "w") as f:
            for row in self.data:
                f.write(" ".join(map(str, row)) + "\n")


class PrintMixin:
    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.data])


class PropertyMixin:
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = np.array(value)


class NumPyArray(ArithmeticMixin, SaveFileMixin, PrintMixin, PropertyMixin):
    def __init__(self, data):
        self.data = data


def main():
    np.random.seed(0)
    matrix1 = NumPyArray(np.random.randint(0, 10, (10, 10)))
    matrix2 = NumPyArray(np.random.randint(0, 10, (10, 10)))

    matrix_sum = matrix1 + matrix2
    matrix_elementwise = matrix1 * matrix2
    matrix_mul = matrix1 @ matrix2

    matrix_sum.save_to_file("matrix+_task2.txt")
    matrix_elementwise.save_to_file("matrix*_task2.txt")
    matrix_mul.save_to_file("matrix@_task2.txt")


if __name__ == "__main__":
    main()
