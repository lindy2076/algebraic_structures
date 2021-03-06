import colorama
from copy import deepcopy
from colorama import Fore, Back, Style
from properties_check import *

colorama.init()
st_reset = Style.RESET_ALL

# для repr класса sw
OPERATORS = ['+', '*', '^', '$']
# все существующие свойства таблицы
PROPERTIES = ['associativity', 'commutativity', 'l_distr', 'r_distr', 'l_absorb', 'r_absorb',
              'idem', 'l_neutral', 'r_neutral', 'l_contractility', 'r_contractility',
              'l_inverse', 'r_inverse', 'solv']
# свойства одной таблицы
SINGLE_PROPERTIES = ['associativity', 'commutativity', 'idem', 'l_neutral', 'r_neutral',
                     'l_contractility', 'r_contractility', 'l_inverse', 'r_inverse', 'solv']
# свойства двух таблиц
DOUBLE_PROPERTIES = ['l_distr', 'r_distr', 'l_absorb', 'r_absorb']


def colored(text: str, color: str, backcolor: str = None) -> str:
    c = Fore.BLACK
    bc = ''
    if color == "g":
        c = Fore.GREEN
    if color == "r":
        c = Fore.RED
    if color == "b":
        c = Fore.BLUE
    if color == "y":
        c = Fore.YELLOW
    if color == "m":
        c = Fore.MAGENTA
    if backcolor:
        if backcolor == "g":
            bc = Back.GREEN
        if backcolor == "w":
            bc = Back.WHITE
        if backcolor == "b":
            bc = Back.BLUE
        if backcolor == "y":
            bc = Back.YELLOW
        if backcolor == "m":
            bc = Back.MAGENTA

    return str(c + bc + text + st_reset)


# TODO вроде класс готов, но пока никак не используется. Надо ещё structure_state переписать
class SW:
    def __init__(self, *tables):
        self.tables = []
        for table in tables:
            self.tables.append(table)
        self.n = len(self.tables[0])  # можность множества
        self.set = [x for x in range(self.n)]  # множество
        self.table_properties = [[] for _ in range(len(tables))]  # список списков свойств таблиц. Последние свойства -
        # - дистрибутивность и поглощение попарно всех таблиц. ...[T, T, F, F, (id1, id2)], [F, T, F, F, (id2, id3)]...
        self.table_types = []  # типы структур таблиц
        self.structure_type = None  # тип структуры

    def __repr__(self):
        res = ''
        for ind in range(len(self.tables)):
            i = ind
            if i >= len(OPERATORS):
                i = 0
            res += colored(OPERATORS[i], 'y') + ' '
            i += 1
            for elem in self.set:
                res += str(elem) + ' '
            res += colored('|  ', 'r')
        res += '\n'
        for j in range(self.n):
            for table in self.tables:
                res += str(j) + ' '
                res += colored(' '.join(map(str, table[j])), 'b') + colored(' |  ', 'r')
            res += '\n'
        return res

    def change_set(self, new_set_):  # меняет обёрточное множество(которое будет выводиться)
        if len(new_set_) != len(self.set):
            print('длина нового множества не совпадает с длиной старого.')
        else:
            self.set = new_set_

    def table_state(self, table_number=0):  # проверка всех свойств одной таблицы и их вывод
        table = self.tables[table_number]
        set_len = len(table)  # self.n?
        table_props = [0] * 10
        print('-'*40 + '\nProperties of table № ' + str(table_number))
        for index, propty in enumerate(SINGLE_PROPERTIES):
            res = table_property_check(propty, set_len, table)
            res_color = 'g' if (res is not False and res != -1) else 'r'
            print(colored(propty + ': ', 'y') + colored(str(res), res_color))
            table_props[index] = res
        print('-'*40)
        self.table_properties[table_number] = table_props
        return table_props

    def structure_state(self):  # проверка всех свойств всех таблиц, запись в self.table_properties, self.table_types
        tables_amount = len(self.tables)
        # определяем свойства всех таблиц
        for i in range(tables_amount):  # свойства таблиц по отдельности
            self.table_properties[i] = self.table_state(i)
        for i in range(tables_amount):  # дистрибутивность, поглощение
            for j in range(tables_amount):
                self.table_properties.append(self.pair_tables_check(i, j))

        # проверили все свойства, теперь определяем типы отдельных таблиц
        for table_prop in self.table_properties:
            for index, str_prop in enumerate(ONE_OPERATION_STRUCTURE_PROPERTIES):
                if table_prop == str_prop:
                    structure_type = ONE_OPERATION_STRUCTURE_TYPES[index]
                    self.table_types.append(structure_type)
        # выяснили все типы таблиц, теперь можно проверить тип структур, которые они образуют:

        return self.table_properties

    def pair_tables_check(self, first_table_index, second_table_index):  # проверка дистр, поглощения
        double_properties = []
        for index, propty in enumerate(DOUBLE_PROPERTIES):
            res = table_property_check(propty, self.n, self.tables[first_table_index], self.tables[second_table_index])
            double_properties.append(res)
        double_properties.append((first_table_index, second_table_index))  # [T, T, T, T, (2, 5)] kinda
        return double_properties


def table_property_check(prop='associativity', n=0, *tables):  # проверка свойства prop данной таблицы(двух для a3 a4)
    if tables and n:
        table = tables[0]
    else:
        return -2
    res = 'invalid prop'
    if prop == PROPERTIES[0]:
        res = associtiativity(table, n)
    elif prop == PROPERTIES[1]:
        res = commutativity(table, n)
    elif prop == PROPERTIES[6]:
        res = idempotence(table, n)
    elif prop == PROPERTIES[7]:
        res = left_neutral(table, n)
    elif prop == PROPERTIES[8]:
        res = right_neutral(table, n)
    elif prop == PROPERTIES[9]:
        res = left_contractility(table, n)
    elif prop == PROPERTIES[10]:
        res = right_contractility(table, n)
    elif prop == PROPERTIES[11]:
        ln = left_neutral(table, n)
        if ln == right_neutral(table, n) and ln != -1:  # есть нейтральный
            res = left_inverse(table, n, ln)
        else:
            res = False
    elif prop == PROPERTIES[12]:
        ln = left_neutral(table, n)
        if ln == right_neutral(table, n) and ln != -1:
            res = right_inverse(table, n, ln)
        else:
            res = False
    elif prop == PROPERTIES[13]:
        res = solvability(table, n)

    elif prop == PROPERTIES[2]:
        res = left_distributivity(tables[0], tables[1], n)
    elif prop == PROPERTIES[3]:
        res = right_distributivity(tables[0], tables[1], n)

    elif prop == PROPERTIES[4]:
        res = left_absorption(tables[0], tables[1], n)
    elif prop == PROPERTIES[5]:
        res = right_absorption(tables[0], tables[1], n)

    return res


# 0: a1; 1: a2; 2: a5; 3 4: a6; 5 6: a7; 7 8: a8; 9: a9;
def table_properties_check(table, n=0):  # возвращает все свойства данной таблицы
    if table and n:
        table_props = [0] * 10  # свойства для таблиц с одной операцией
    else:
        return -1
    for index, propty in enumerate(SINGLE_PROPERTIES):
        table_props[index] = table_property_check(propty, n, table)
    return table_props


def pair_tables_properties_check(table1, table2, n=0):  # возвращает список дистр, поглощения для двух таблиц
    double_properties = []
    for index, propty in enumerate(DOUBLE_PROPERTIES):
        res = table_property_check(propty, n, table1, table2)
        double_properties.append(res)
    return double_properties  # [T T F T]


# a9, a6 => a8; a9 => a7; a1, a8 => a9; a1, a8 => a7;
# две константы-рудимента, раньше была процедура на проверку, в которой они использовались (ещё в классе есть)
ONE_OPERATION_STRUCTURE_TYPES = ['magma',  # none,
                                 'quasigroup', 'unitar_magma', 'semigroup',  # a9, a6, a1
                                 'loop', 'reverse_semigroup', 'monoid',  # a6a9, a1a9, a1a6
                                 'group', 'abel_group', 'abel_group'  # a1a6a9, a1a2a6a9
                                 ]
# a1: 0; a2: 1; a5: 2; a6: 3 4; a7: 5 6; a8: 7 8; a9: 9;
ONE_OPERATION_STRUCTURE_PROPERTIES = [[],  # magma
                                      [5, 6, 9],  # quasigroup
                                      [3, 4],  # unitar magma
                                      [0],  # semigroup
                                      [3, 4, 5, 6, 7, 8, 9],   # loop  ( a9, a6 => a8 )
                                      [0, 5, 6, 9],  # reverse semigroup (обратная полугруппа (с сократимостью))
                                      [0, 3, 4],  # monoid
                                      [0, 3, 4, 5, 6, 7, 8, 9],  # group  2.1.4.7
                                      [0, 1, 3, 4, 5, 6, 7, 8, 9],  # abel_group
                                      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # idem abel_group
                                      ]


def check_structure_with_one_operation(table, n: int, table_props=None):  # TODO нужен тест
    structure_type = 'magma..'
    if not table_props:
        table_props = table_properties_check(table, n)

    if table_props[0]:  # ассоциативна
        structure_type = 'semigroup'
        if table_props[5] and table_props[6] and table_props[9]:  # разрешима
            structure_type = 'reverse semigroup'
            if (table_props[3] != -1) and (table_props[4] != -1):  # нейтральный
                structure_type = 'group'
                if table_props[1]:  # коммутативна
                    structure_type = 'abel_group'
        elif (table_props[3] != -1) and (table_props[4] != -1):
            structure_type = 'monoid'

        if table_props[1] and 'abel_group' not in structure_type:
            structure_type = 'commutative ' + structure_type
        if table_props[2]:
            structure_type = 'idem ' + structure_type

    else:  # не ассоциативна
        if table_props[5] and table_props[6] and table_props[9]:  # разрешима
            structure_type = 'quasigroup'
            if table_props[3] != -1 and table_props[4] != -1:  # нейтральный
                structure_type = 'loop'
        else:
            if table_props[3] != -1 and table_props[4] != -1:
                structure_type = 'unitar_magma'

        if table_props[1]:
            structure_type = 'commutative ' + structure_type
        if table_props[2]:
            structure_type = 'idem ' + structure_type

    return structure_type


def table_shrink_neutral(table, n: int, neutral: int):  # сужение таблицы (без нейтрального)
    if neutral == -1:
        return -1
    table_with_no_neutral = [[0] * (n-1) for _ in range(n-1)]
    table = deepcopy(table)
    for i in range(n - 1):
        for j in range(n - 1):
            index1, index2 = j, i
            if j >= neutral:
                index1 += 1
            if i >= neutral:
                index2 += 1
            if table[index1][index2] >= neutral:
                table[index1][index2] -= 1
            # print(table)
            if table[index1][index2] == -1:
                return -1
            table_with_no_neutral[j][i] = table[index1][index2]

    return table_with_no_neutral


# возвращает тип структуры по двум таблицам
def check_structure_with_two_operations(table1, table2, n: int, print_solo_structures=False):
    # положим первую операцию сложением, а вторую умножением
    algebra_type = 'nothing'
    double_properties1 = pair_tables_properties_check(table2, table1, n)
    type1 = check_structure_with_one_operation(table1, n)
    type2 = check_structure_with_one_operation(table2, n)
    if print_solo_structures:
        print('типы таблиц: ', colored(type1, '', 'w'), 'and', colored(type2, '', 'w'))

    if double_properties1[0:2] == [True, True]:  # вторая дистр относительно первой
        if type1 == 'abel_group' and 'semigroup' in type2:
            algebra_type = 'ring'
        elif type1 == 'abel_group' and 'monoid' in type2:
            algebra_type = 'ring with neutral'

        # проверяем на поле и тело
        table1_neutral = table_property_check('l_neutral', n, table1) == table_property_check('r_neutral', n, table1)
        table1_neutral = (-1, table_property_check('l_neutral', n, table1))[table1_neutral]
        table2_with_no_neutral = table_shrink_neutral(table2, n, table1_neutral)  # сужаем таблицу (без 0)
        if table2_with_no_neutral == -1:
            return algebra_type  # не получается поле
        type2 = check_structure_with_one_operation(table2_with_no_neutral, n - 1)
        if print_solo_structures:
            print('вторая операция без нейтрального образует ' + colored(type2, '', 'w'))
        if type1 == 'abel_group' and type2 == 'group':
            algebra_type = 'division ring'
        if type1 == 'abel_group' and 'abel_group' in type2:
            algebra_type = 'field'
    else:  # не дистрибутивно
        if print_solo_structures:
            print('не дистибутивны..')
        pass
    return algebra_type


def print_table_properties(table, n: int):
    table_props = [0] * 10
    print('-' * 40 + '\nProperties of the table:')
    for index, propty in enumerate(SINGLE_PROPERTIES):
        res = table_property_check(propty, n, table)
        res_color = 'g' if (res is not False and res != -1) else 'r'
        print(colored(propty + ': ', 'y') + colored(str(res), res_color))
        table_props[index] = res
    print('-' * 40)
    return table_props
