from copy import deepcopy
import numpy as np


class WriteInFileMixin:
    def write_in_file(self, path):
        with open(path, 'w') as f:
            f.write(str(self))


class MatrixStrMixin:
    def __str__(self):
        return '\n'.join('\t'.join(map(str, row)) for row in self.value)


class Matrix(WriteInFileMixin, MatrixStrMixin):
    def __init__(self, arr, *, copy=False, skip_check=False):
        self.rows = len(arr)
        self.cols = len(arr[0])
        self.shape = (self.rows, self.cols)
        if not skip_check:
            assert all(len(row) == self.cols for row in arr)
        self.value = arr if not copy else deepcopy(arr)

    def __add__(self, other):
        assert self.shape == other.shape
        return Matrix([[i + j for i, j in zip(row1, row2)] for row1, row2 in zip(self.value, other.value)],
                      skip_check=True)

    def __mul__(self, other):
        assert self.shape == other.shape
        return Matrix([[i * j for i, j in zip(row1, row2)] for row1, row2 in zip(self.value, other.value)],
                      skip_check=True)

    def __matmul__(self, other):
        assert self.cols == other.rows
        transposed = list(zip(*other.value))
        return Matrix([[sum(i * j for i, j in zip(row, col)) for col in transposed] for row in self.value],
                      skip_check=True)


if __name__ == '__main__':
    matr_1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matr_2 = Matrix(np.random.randint(0, 10, (10, 10)))
    # print(matr_1, matr_2, sep='\n\n')
    (matr_1 + matr_2).write_in_file('artifacts/easy/matrix+.txt')
    (matr_1 * matr_2).write_in_file('artifacts/easy/matrix_mul.txt')
    (matr_1 @ matr_2).write_in_file('artifacts/easy/matrix@.txt')
