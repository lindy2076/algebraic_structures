import structure
from itertools import combinations
from copy import deepcopy

# короче здесь должно всё основное быть


def generate_table(num: int, size: int) -> list[list]:  # генерация таблицы из её идентификатора
    new_table = [[0] * size for _ in range(size)]
    c, r = size - 1, size - 1
    while num:
        new_table[r][c] = num % size
        if not c:
            c = size
            r -= 1
        c -= 1
        num //= size
    return new_table


def print_table(table, k: int):  # вывод таблицы
    res = '  '
    for i in range(k):
        res += str(i) + ' '
    res += '\n'
    for index, string in enumerate(table):
        res += str(index) + ' '
        for elem in string:
            res += structure.colored(str(elem), 'b') + ' '
        res += '\n'
    print(res)


def print_tables(k: int, *tables):  # принтит если много таблиц в одну строку, к - мощность множества
    res = ''
    for ind in range(len(tables)):
        i = ind
        if i >= len(structure.OPERATORS):
            i = 0
        res += structure.colored(structure.OPERATORS[i], 'y') + ' '
        i += 1
        for elem in range(k):
            res += str(elem) + ' '
        res += structure.colored('|  ', 'r')
    res += '\n'
    for j in range(k):
        for table in tables:
            res += str(j) + ' '
            res += structure.colored(' '.join(map(str, table[j])), 'b') + structure.colored(' |  ', 'r')
        res += '\n'
    print(res)


def move_columns(input_table, size: int, index1: int, index2: int):  # перестановка i, j строк и столбцов местами
    table = deepcopy(input_table)
    if max(index1, index2) >= size:
        print('move_columns invalid indexes')
        return -1
    for i in range(size):
        table[i][index1], table[i][index2] = table[i][index2], table[i][index1]
    for i in range(size):
        table[index1][i], table[index2][i] = table[index2][i], table[index1][i]
    return table


def table_to_num(table, size: int):  # таблица в число, её определяющее
    num = 0
    for i in range(size):
        for j in range(size):
            num += table[i][j] * (size ** (size * size - i * size - j % size - 1))
    return num


def generate_non_isomorf_nums(k: int):  # выдаёт
    repeated_nums = set()
    for num in range(k**(k*k)):
        if num not in repeated_nums:
            yield num
        for indexes in combinations(range(k), 2):
            table = generate_table(num, k)
            new_table = move_columns(table, k, indexes[0], indexes[1])
            isomorf_num = table_to_num(new_table, k)
            # print(isomorf_num)
            if isomorf_num not in repeated_nums:
                repeated_nums.add(isomorf_num)
    # print(repeated_nums)


def main():
    print('приветствие.')
    count = 0
    k = int(input())
    for i in generate_non_isomorf_nums(k):  # смотрим на таблицы просто что каждая из себя представляет
        table = generate_table(i, k)
        # print_table(table, k)
        # print(structure.check_structure_with_one_operation(table, k))
        # print('-'*40)
        count += 1
    print(count, k**(k*k))

    alg_types = {}
    for num1 in generate_non_isomorf_nums(k):
        for num2 in generate_non_isomorf_nums(k):
            table1, table2 = generate_table(num1, k), generate_table(num2, k)
            # print_tables(k, table1, table2)
            alg_type = structure.check_structure_with_two_operations(table1, table2, k)
            # print(alg_type)
            if alg_type not in alg_types:
                alg_types[alg_type] = 0
            else:
                alg_types[alg_type] += 1
            if alg_type != 'nothing':
                alg_types[alg_type + str(num1)] = [num1, num2]
            # print('-'*40)
    print(alg_types)


if __name__ == '__main__':
    main()
