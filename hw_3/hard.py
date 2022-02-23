from medium import MyArr
import numpy as np
from numpy.random import randint


class MatrixHash:
    def __hash__(self):
        # somewhat resembles hash function for tuples
        # https://github.com/python/cpython/blob/24a549fcea682b8de88adf79924ccbc3a448cb0d/Objects/tupleobject.c#L348
        x = 345678  # just some number
        p = 2**35  # upper bound for hash
        mult = 1000003  # just another number
        add = self.value.shape[0] * self.value.shape[1]
        for row in self.value:
            for val in row:
                # val % p is used instead of hash(p)
                x = ((x ^ (val % p)) * mult) % p  # xor with hash of number -> multiply -> mod
                mult += add + 82520  # just another number
        return int(x)

    def __eq__(self, other):
        return self.value == other.value


class MyMatrix(MyArr, MatrixHash):
    products = {}

    def __matmul__(self, other):
        try:
            return MyMatrix.products[(self, other)]
        except KeyError:
            res = super().__matmul__(other)
            MyMatrix.products[(self, other)] = res
            return res

    __hash__ = MatrixHash.__hash__


def get_rand(size, mx=10):
    return randint(0, mx, (size, size), dtype=np.int64)


def find_collisions():
    class broken_array(list):
        def __new__(cls, arr):
            return list.__new__(broken_array, arr)

    size = 10
    arr1 = broken_array(get_rand(size))
    arr2 = broken_array(get_rand(size))
    arr1.shape = arr2.shape = (size + 1, size)
    matr = MyMatrix([])

    matr.value = arr1
    arr1.append([hash(matr)] + [1] * (size - 1))
    A = MyMatrix(arr1)

    matr.value = arr2
    arr2.append([hash(matr)] + [1] * (size - 1))
    C = MyMatrix(arr2)
    return A, C


def main():
    A, C = find_collisions()
    print(A, C, sep='\n\n')
    print(hash(A), hash(C))
    A.write_into_file('artifacts/hard/A.txt')
    C.write_into_file('artifacts/hard/C.txt')
    B = MyMatrix(get_rand(10))
    B.write_into_file('artifacts/hard/B.txt')
    B.write_into_file('artifacts/hard/D.txt')  # does not make much sense though
    (A @ B).write_into_file('artifacts/hard/AB.txt')
    (C @ B).write_into_file('artifacts/hard/CD.txt')
    with open('artifacts/hard/hash.txt', 'w') as f:
        f.write(f'{hash(A @ B)} {hash(C @ B)}')  # black magic happens here


if __name__ == '__main__':
    main()
