import numpy


def main():
    # warmup 1
    arr = numpy.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print('Numpy matrix:\n{}'.format(arr))
    rank = numpy.linalg.matrix_rank(arr)
    print('Rank: {}'.format(rank))
    determinant = numpy.linalg.det(arr)
    print('Determinant: {}'.format(determinant))
    inverse = numpy.linalg.inv(arr)
    print('Inverse:\n{}'.format(inverse))

    # warmup 2
    # 3x + y = 9 and x + 2y = 8:
    coefficients = numpy.array([[3, 1], [1, 2]])
    values = numpy.array([9, 8])
    solved = numpy.linalg.solve(coefficients, values)
    print('Solved equation:\n{}'.format(solved))


if __name__ == '__main__':
    main()
