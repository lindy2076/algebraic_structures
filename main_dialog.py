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


def convert_string_to_num(table_child: str):  # переводим строку цифр в таблицу
    table_sep = table_child.split()
    if not table_child:
        return -1
    if len(table_sep) > 100:
        return -2
    for set_len in range(10):
        if len(table_sep) <= set_len * set_len:
            break
    result = 0
    for i in range(len(table_sep), 0, -1):
        if not is_int(table_sep[i - 1]):
            return -3
        elif int(table_sep[i - 1]) >= set_len:
            return -4
        else:
            result += int(table_sep[len(table_sep) - i]) * (set_len ** (i - 1))

    return result, set_len


PERMUTATIONS_FOR_3LEN_SET = [(0, 1), (0, 2), (1, 2), [(0, 1), (1, 2)], [(1, 2), (0, 1)]]


def generate_non_isomorf_nums(k: int):  # k = 2, 3 only
    repeated_nums = set()
    for num in range(k ** (k * k)):
        if num not in repeated_nums:
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


def print_info():  # выводит информацию о программе
    print('Эта программа - песочница, в которой можно играть таблицами Кэли и проверять их свойства + какие' +
          ' алгебраические структуры они образуют.')
    print('В программе все таблицы должны быть приведены к следующему виду: все переменные переименованы в числа от ' +
          '0 до мощности множества - 1. Строки и столбцы должны быть расположены' +
          ' в порядке возрастания индексов(0 1 2 ...). ')
    print('')
    print('В программе предусмотрена проверка свойств для таблиц на множествах мощности < 10.\n')
    print('Проверка ВСЕХ неизоморфных таблиц рассчитана для манипуляций на двух- и трёхэлементных множествах.')
    print('На четырёхэлементном множестве существует около 4 миллиардов операций и проверка всех операций занимает' +
          ' огромное(буквально) количество времени и оперативной памяти. Нужно около 90 гигабайт оперативной памяти' +
          '. Не рекомендую. Жмите ctrl+c, если решили попробовать.')
    print('Lindy2076 2022.')


def print_help():  # выводит списки команд
    print(structure.colored('команды:', 'y'))
    print('Далее ' + structure.colored('n, table_num', 'b', 'w') + '(если они встречаются вместе) будут обозначать' +
          ' идентификатор таблицы и её номер соответственно.')
    print('Если команда написана через ' + structure.colored('/', '', 'w') + ' то можно выбрать один из вариантов\n')

    print(structure.colored('help', 'g') + '/' + structure.colored('h', 'g') + ' - вывод списка команд')
    print(structure.colored('num', 'g') + '/' + structure.colored('n', 'g') +
          ' - выдает номер, кодирующий введённую строкой таблицу. Значения следует вводить через пробел.')
    print(structure.colored('print', 'g') + '/' + structure.colored('p', 'g') +
          structure.colored(' n, table_num', 'b') + ' - вывод таблицы под её номером на множестве мощности n')
    print(structure.colored('solo', 'g') + ' - список типов алгебраических структур с одной операцией на всех' +
          ' неизоморфных таблицах операции на n-элементном множестве')
    print(structure.colored('double', 'g') + ' -список типов алгебраических структур с двумя операциями на всех' +
          ' неизоморфных таблицах операции на n-элементном множестве')
    print(structure.colored('type', 'g') + '/' + structure.colored('t', 'g') + structure.colored(' n, table_num', 'b') +
          ' - пишет свойства и тип таблицы')
    print('-'*40)
    print(structure.colored('temp', 'g') + ' - выводит список таблиц в памяти')
    print(structure.colored('add', 'g') + '/' + structure.colored('a', 'g') + structure.colored(' n, table_num', 'b') +
          ' - добавляет таблицу в память')
    print(structure.colored('del', 'g') + structure.colored(' n', 'b') +
          ' - удаляет таблицу под индексом n из памяти')
    print(structure.colored('mix', 'g') + structure.colored(' a b', 'b') +
          ' - выводит тип алгебраической структуры, которая получается из таблиц a и b из памяти')

    print(structure.colored('info', 'g') + ' - о программе')
    print(structure.colored('q', 'g') + ' - выход')


def is_int(num: str):  # True если int
    try:
        int(num)
    except ValueError:
        return 0
    return 1


# список доступных команд (чтобы вывести сообщение о несуществующей в основном цикле)
COMMANDS = ['h', 'help', 'q', 'solo', 'double', 'p', 'print', 't', 'type', 'a', 'add', 'del', 'temp', 'mix', 'info',
            'num', 'n']


def main():
    print('приветствие')
    command = 0
    temp = []
    while command != 'q':
        command_ = input(':|').lower().split()
        command = command_[0]
        command_.append([])  # FIXME костыль
        command_.append([])
        print()

        if command not in COMMANDS:
            print('странная команда... попробуйте help')

        if command == 'h' or command == 'help':
            print_help()

        if command == 'info':
            print_info()

        if command == 'p' or command == 'print':  # [1] - мощность, [2] - номер таблицы

            if not command_[1] or not is_int(command_[1]) or not command_[2] or not is_int(command_[2]):
                print('плохой инпут...')
            else:
                table_num, set_size = int(command_[2]), int(command_[1])
                if set_size > 10:
                    print('слишком большой размер множества')
                else:
                    if table_num >= set_size**(set_size*set_size) or table_num < 0:
                        print('номер таблицы довольно странный')
                    else:
                        table = generate_table(table_num, set_size)
                        print_table(table, set_size)

        if command == 'n' or command == 'num':
            print('введите таблицу в строку через пробелы. (Пример: 0 1 0 1)')
            prob_table = input('>')
            conv_res, conv_res_set_len = convert_string_to_num(prob_table)
            if conv_res == -1:
                print('надо было ввести таблицу')
            elif conv_res == -2:
                print('размеры таблицы не более 10х10')
            elif conv_res == -3:
                print('элементы таблицы должны быть цифрами')
            elif conv_res == -4:
                print('элементы таблицы должны быть меньше мощности множества')
            else:
                print('Таблица кодируется числом ' + str(conv_res))
                print('Таблица: ')
                table = generate_table(conv_res, conv_res_set_len)
                print_table(table, conv_res_set_len)

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
                num1, num2 = 0, 0
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

                print(structure.colored('типы и сколько:', 'y'))
                for alg_type in alg_types:
                    print('  ', alg_type, ': ', alg_types[alg_type])
                print(structure.colored('какие номера образуют тип алгебры:', 'y'))
                for alg_type in more_info:
                    print('  ', alg_type, ': ', *more_info[alg_type])

        if command == 'type' or command == 't':
            if not command_[1] or not is_int(command_[1]) or not command_[2] or not is_int(command_[2]):
                print('плохой инпут...')
            else:
                table_num, set_size = int(command_[2]), int(command_[1])
                if set_size > 10:
                    print('слишком большой размер множества')
                else:
                    if table_num >= set_size ** (set_size * set_size) or table_num < 0:
                        print('номер таблицы довольно странный')
                    else:
                        table = generate_table(table_num, set_size)
                        print_table(table, set_size)
                        table_props = structure.print_table_properties(table, set_size)
                        print(structure.check_structure_with_one_operation(table, set_size, table_props))

        if command == 'temp':
            if temp:
                for index, table_data in enumerate(temp):
                    print('таблица номер ' + str(index) + '(кодируется числом ' + str(table_data[1]) + '):')
                    print_table(table_data[0], len(table_data[0]))
            else:
                print('в temp пусто.. добавьте таблицу с помощью add')

        if command == 'del':
            try:
                temp.pop(int(command_[1]))
            except IndexError:
                print('таблиц меньше..')
            except ValueError:
                print('введите номер корректно..')
            except TypeError:
                print('не ввели номер..')
            else:
                print('таблица удалена')

        if command == 'add' or command == 'a':
            if not command_[1] or not is_int(command_[1]) or not command_[2] or not is_int(command_[2]):
                print('плохой инпут...')
            else:
                table_num, set_size = int(command_[2]), int(command_[1])
                if set_size > 10:
                    print('слишком большой размер множества')
                else:
                    if table_num >= set_size ** (set_size * set_size) or table_num < 0:
                        print('номер таблицы довольно странный')
                    else:
                        table = generate_table(table_num, set_size)
                        temp.append((table, table_num))
                        print('таблица номер ' + str(table_num) + ' успешно добавлена в память')

        if command == 'mix':
            if not command_[1] or not is_int(command_[1]) or not command_[2] or not is_int(command_[2]):
                print('плохой инпут...')
            else:
                table1_index, table2_index = int(command_[1]), int(command_[2])
                try:
                    table1, table2 = temp[table1_index][0], temp[table2_index][0]
                except IndexError:
                    print('таблицы ' + str((table1_index, table2_index)[table2_index >= len(temp)]) + ' нету в памяти')
                except Exception as wtf:
                    print('oh.. mix error ' + str(wtf.__class__))
                else:
                    if len(table1) != len(table2):
                        print('таблицы не одинаковых размеров...')
                    else:
                        print_tables(len(table1), table1, table2)
                        alg_type = structure.check_structure_with_two_operations(table1, table2, len(table1), True)
                        print('эти таблицы образуют ' + structure.colored(alg_type, 'g', 'w'))

        print('-'*40)


if __name__ == '__main__':
    main()
