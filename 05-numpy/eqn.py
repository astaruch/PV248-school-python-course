from sys import argv
import numpy
from collections import OrderedDict


def main():
    filename = argv[1]
    with open(filename, 'r') as f:
        lines = f.readlines()
        equations = []
        constants = []
        distinct_variables = ''
        num_of_equations = 0
        for line in lines:
            if not line:
                continue
            num_of_equations = num_of_equations + 1
            coefficients, constant = line.split('=')
            constants.append(int(constant))
            var = ''
            vars = []
            for letter in coefficients:
                if letter == ' ':
                    if var == '-' or var == '':
                        continue
                    vars.append(var)
                    var = ''
                    continue
                elif letter == '+':
                    continue
                elif letter == '-':
                    var = '-'
                    continue
                else:
                    # letter or digit
                    if (var == '' or var == '-') and letter.isalpha():
                        var = var + '1'
                    var = var + letter
                    if letter.isalpha() and letter not in distinct_variables:
                        distinct_variables = distinct_variables + letter
            equations.append(vars)
        distinct_variables = ''.join(sorted(distinct_variables))
        # print(distinct_variables)

        coefficients_for_variables = OrderedDict()
        for variable in distinct_variables:
            coefficients_for_variables[variable] = []
            for equation in equations:
                found = list(filter(lambda x: variable in x, equation))
                if found:
                    # removing letter from list: ['-2x'] => -2
                    found = int(found[0][:-1])
                else:
                    # not found so in numpy array it will be zero
                    found = 0
                coefficients_for_variables[variable].append(found)
        # print(coefficients_for_variables)

        coefficients_for_equations = OrderedDict()
        for i in range(0, num_of_equations):
            coefficients_for_equations[str(i)] = []
            for variable in distinct_variables:
                coefficients_for_equations[str(i)].append(
                    coefficients_for_variables[variable][i])
        # print(coefficients_for_equations)

        list_of_coefficients = []
        for i in range(0, num_of_equations):
            list_of_coefficients.append(coefficients_for_equations[str(i)])
        # print(list_of_coefficients)

        np_coefficients = numpy.array(list_of_coefficients)
        np_constants = numpy.array(constants)
        try:
            solved = numpy.linalg.solve(np_coefficients, np_constants)
            str_solutions = []
            for (idx, variable) in enumerate(distinct_variables):
                str_solution = variable + ' = ' + str(solved[idx])
                str_solutions.append(str_solution)
            print('solution: {}'.format(', '.join(str_solutions)))
        except numpy.linalg.LinAlgError:
            rank = numpy.linalg.matrix_rank(np_coefficients)
            print('solution space dimension: {}'.format(
                len(distinct_variables) - rank))


if __name__ == '__main__':
    main()
