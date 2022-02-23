from copy import deepcopy
import numpy as np


class WriteInFileMixin:
    def write_in_file(self, path):
        with open(path, 'w') as f:
            f.write(str(self))


class MatrixStrMixin:
    def __str__(self):
        return self._create_str(self.value, self._calc_dim())

    def _create_str(self, value, depth):
        if depth == 1:
            return '\t'.join(map(str, value))
        return ('\n' * (depth - 1)).join(self._create_str(subarr, depth - 1) for subarr in value)

    def _calc_dim(self):
        dim = 0
        val = self.value
        try:
            while len(val):
                val = val[0]
                dim += 1
        except TypeError:
            return dim


class Matrix(WriteInFileMixin, MatrixStrMixin):
    def __init__(self, arr, *, copy=False, skip_check=False):
        self._rows = len(arr)
        self._cols = len(arr[0])
        self._shape = (self._rows, self._cols)
        if not skip_check:
            assert all(len(row) == self._cols for row in arr)
        self.value = arr if not copy else deepcopy(arr)

    def __add__(self, other):
        assert self._shape == other._shape
        return Matrix([[i + j for i, j in zip(row1, row2)] for row1, row2 in zip(self.value, other.value)],
                      skip_check=True)

    def __mul__(self, other):
        assert self._shape == other._shape
        return Matrix([[i * j for i, j in zip(row1, row2)] for row1, row2 in zip(self.value, other.value)],
                      skip_check=True)

    def __matmul__(self, other):
        assert self._cols == other._rows
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
