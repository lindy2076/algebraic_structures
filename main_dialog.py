import structure
from itertools import combinations
from copy import deepcopy

# короче здесь должно всё основное быть


# --------------------------- вычислительные функции -------------------------
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


def table_to_num(table, size: int):  # перевод таблицы в определяющее её число
    num = 0
    for i in range(size):
        for j in range(size):
            num += table[i][j] * (size ** (size * size - i * size - j % size - 1))
    return num


def generate_non_isomorf_nums(k: int):  # выдаёт неизоморфные номера таблиц на k-элементном множестве  # FIXME тяжко
    repeated_nums = set()
    for num in range(k**(k*k)):
        if num not in repeated_nums:
            yield num
        else:
            repeated_nums.remove(num)
        for indexes in combinations(range(k), 2):
            table = generate_table(num, k)
            new_table = move_columns(table, k, indexes[0], indexes[1])
            isomorf_num = table_to_num(new_table, k)
            # print(isomorf_num)
            if isomorf_num not in repeated_nums and isomorf_num > num:
                repeated_nums.add(isomorf_num)
    # print(repeated_nums)


PERMUTATIONS_FOR_3LEN_SET = [(0, 1), (0, 2), (1, 2), [(0, 1), (1, 2)], [(1, 2), (0, 1)]]


def generate_non_isomorf_nums_fixed(k: int):  # костыль
    repeated_nums = set()
    for num in range(k ** (k * k)):
        if num not in repeated_nums:  # число неизоморфно ничему
            yield num
        else:
            repeated_nums.remove(num)

        if k == 2:
            for indexes in combinations(range(k), 2):
                table = generate_table(num, k)
                new_table = move_columns(table, k, indexes[0], indexes[1])
                isomorf_num = table_to_num(new_table, k)
                if isomorf_num not in repeated_nums and isomorf_num > num:
                    repeated_nums.add(isomorf_num)
        elif k == 3:
            for permutation in PERMUTATIONS_FOR_3LEN_SET:
                table = generate_table(num, k)
                if type(permutation) is not tuple:
                    for indexes in permutation:
                        new_table = move_columns(table, k, indexes[0], indexes[1])

                        isomorf_num = table_to_num(new_table, k)
                        if isomorf_num not in repeated_nums and isomorf_num > num:
                            repeated_nums.add(isomorf_num)
                else:
                    new_table = move_columns(table, k, permutation[0], permutation[1])

                    isomorf_num = table_to_num(new_table, k)
                    if isomorf_num not in repeated_nums and isomorf_num > num:
                        repeated_nums.add(isomorf_num)


def put_non_isomorf_nums_in_file(k: int):  # создаёт файл с неизоморфными номерами таблиц
    f = open("nonIsomorfNums_" + str(k) + ".txt", 'w')
    for number in generate_non_isomorf_nums(k):
        f.write(str(number) + '\n')
    f.close()
    print('файл для k=' + str(k) + ' создан')


def get_non_isomorf_nums(k: int):
    try:
        f = open("nonIsomorfNums_" + str(k) + ".txt", 'r')
    except FileNotFoundError:
        put_non_isomorf_nums_in_file(k)  # создаём файлик с неизоморфными номерами таблиц
        f = open("nonIsomorfNums_" + str(k) + ".txt", 'r')

    number = f.readline()
    if not number:
        put_non_isomorf_nums_in_file(k)
    else:
        while number:
            yield int(number)
            number = f.readline()


def get_solo_types(k: int):  # возвращает списки типов алгебр с одной операцией на всех k эл множествах
    alg_types = {}
    more_info = {}

    try:
        for table_num in get_non_isomorf_nums(k):
            table = generate_table(table_num, k)
            alg_type = structure.check_structure_with_one_operation(table, k)
            if alg_type != 'magma..':
                if alg_type not in alg_types:
                    alg_types[alg_type] = 1
                    more_info[alg_type] = []
                else:
                    alg_types[alg_type] += 1
                more_info[alg_type].append(table_num)
    except KeyboardInterrupt:
        print('прервано...')
        return alg_types, more_info

    return alg_types, more_info


# -----------------------------вспомогательные функции-----------------------------------------------------------------

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


def print_help():  # выводит списки команд
    print(structure.colored('команды:', 'y'))
    print(structure.colored('help', 'g') + '/' + structure.colored('h', 'g') + ' - вывод списка команд')
    print(structure.colored('print', 'g') + '/' + structure.colored('p', 'g') +
          structure.colored(' table_num, n', 'b') + ' - вывод таблицы № table_num на множестве мощности n')
    print(structure.colored('props', 'g') + structure.colored(' table_num, n', 'b') +
          ' - вывод свойств таблицы номер table_num на множестве мощности n')
    print(structure.colored('solo', 'g') + ' - список типов алгебраических структур с одной операцией на всех' +
          ' неизоморфных таблицах операции на n-элементном множестве')
    print(structure.colored('double', 'g') + ' -')
    print(structure.colored('q', 'g') + ' - выход')


def is_int(num: str):  # True если int
    try:
        int(num)
    except ValueError:
        return 0
    return 1


def test():
    put_non_isomorf_nums_in_file(2)
    for number in get_non_isomorf_nums(3):
        print(number)
    print('test mode.')
    count = 0
    k = int(input())
    for i in get_non_isomorf_nums(k):  # смотрим на таблицы просто что каждая из себя представляет
        table = generate_table(i, k)
        # print_table(table, k)
        # print(structure.check_structure_with_one_operation(table, k))
        # print('-'*40)
        count += 1
    print(count, k**(k*k))

    alg_types = {}  # type, count
    more_info = {}  # type, num1, num2
    try:
        for num1 in generate_non_isomorf_nums(k):
            for num2 in generate_non_isomorf_nums(k):
                table1, table2 = generate_table(num1, k), generate_table(num2, k)
                # print_tables(k, table1, table2)
                alg_type = structure.check_structure_with_two_operations(table1, table2, k)
                # print(alg_type)
                if alg_type != 'nothing':
                    if alg_type not in alg_types:
                        alg_types[alg_type] = 1
                        more_info[alg_type] = []
                    else:
                        alg_types[alg_type] += 1

                    more_info[alg_type].append((num1, num2))
                # print('-'*40)
    except KeyboardInterrupt:
        print(alg_types, num1, num2)
        print(more_info)
    print(alg_types)
    print(more_info)


# список доступных команд (чтобы вывести сообщение о несуществующей в основном цикле)
COMMANDS = ['h', 'help', 'q', 'solo', 'double', 'p', 'print']


def main():
    print('приветствие')
    command = 0
    while command != 'q':
        command_ = input(':|').split()
        command = command_[0]
        print()

        if command not in COMMANDS:
            print('странная команда... попробуйте help')

        if command == 'h' or command == 'help':
            print_help()

        if command == 'p' or command == 'print':  # [1] - мощность, [2] - номер таблицы
            if not command_[1] or not is_int(command_[1]) or not command_[2] or not is_int(command_[2]):
                print('налажал в инпуте...')
            else:
                table_num, set_size = int(command_[2]), int(command_[1])
                if set_size > 10:
                    print('слишком большой размер')
                else:
                    if table_num >= set_size**(set_size*set_size):
                        print('номер таблицы довольно странный')
                    else:
                        table = generate_table(table_num, set_size)
                        print_table(table, set_size)

        if command == 'solo':
            print('введите мощность множества')
            n = input('n:=')
            if not is_int(n) or int(n) < 1:
                print('странная мощность...')
            else:
                n = int(n)
                alg_types, more_info = get_solo_types(n)

                print(structure.colored('типы и сколько:', 'y'))
                for alg_type in alg_types:
                    print('  ', alg_type, ': ', alg_types[alg_type])
                # print(alg_types)
                print(structure.colored('какие номера образуют тип алгебры:', 'y'))
                for alg_type in more_info:
                    print('  ', alg_type, more_info[alg_type])
                # print(more_info)

        if command == 'double':
            print('введите мощность множества')
            n = input('n:=')
            if not is_int(n) or int(n) < 1:
                print('странная мощность...')
            else:
                n = int(n)

                table1_alg_types, table1_more_info = get_solo_types(n)
                table1_abel_groups, table1_idem_abel_groups = [], []
                if 'abel_group' in table1_alg_types:
                    table1_abel_groups = table1_more_info['abel_group']
                if 'idem abel_group' in table1_alg_types:
                    table1_idem_abel_groups = table1_more_info['idem_abel_group']
                table1_abel_groups = table1_abel_groups + table1_idem_abel_groups

                alg_types = {}
                more_info = {}
                try:
                    for num1 in table1_abel_groups:
                        for num2 in get_non_isomorf_nums(n):
                            table1, table2 = generate_table(num1, n), generate_table(num2, n)

                            alg_type = structure.check_structure_with_two_operations(table1, table2, n)

                            if alg_type != 'nothing':
                                if alg_type not in alg_types:
                                    alg_types[alg_type] = 1
                                    more_info[alg_type] = []
                                else:
                                    alg_types[alg_type] += 1

                                more_info[alg_type].append((num1, num2))
                except KeyboardInterrupt:
                    print('прервано...')
                    print(num1, num2)
                print(alg_types)
                print(more_info)

        print('-'*40)


if __name__ == '__main__':
    # test()
    main()
