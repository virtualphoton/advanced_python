import numpy as np
import numbers

from easy import MatrixStrMixin, WriteIntoFileMixin
from numpy.lib.mixins import NDArrayOperatorsMixin


class MyArr(NDArrayOperatorsMixin, MatrixStrMixin, WriteIntoFileMixin):
    def __init__(self, value):
        self.value = np.asarray(value)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        # just copied from https://numpy.org/doc/stable/reference/generated/numpy.lib.mixins.NDArrayOperatorsMixin.html
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (MyArr,)):
                return NotImplemented

        inputs = tuple(x.value if isinstance(x, MyArr) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, MyArr) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


if __name__ == '__main__':
    matr_1 = MyArr(np.random.randint(0, 10, (10, 10)))
    matr_2 = MyArr(np.random.randint(0, 10, (10, 10)))
    # print(matr_1, matr_2, sep='\n\n')
    (matr_1 + matr_2).write_into_file('artifacts/medium/matrix+.txt')
    (matr_1 * matr_2).write_into_file('artifacts/medium/matrix_mul.txt')
    (matr_1 @ matr_2).write_into_file('artifacts/medium/matrix@.txt')
