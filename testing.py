from structure import *
from properties_check import *
import main_dialog as md


def test_class_init_and_display():  # ok
    table1 = [
        [0, 1, 2],
        [2, 1, 0],
        [2, 2, 2]
    ]
    table2 = [
        [0, 0, 0],
        [1, 0, 2],
        [1, 1, 2]
    ]
    table3 = [
        [1, 1, 0],
        [2, 2, 1],
        [0, 1, 0]
    ]
    a = SW(table1, table2, table3, table1, table2)
    print(a.tables)
    print(a.n)
    print(a.set)
    print(a)
    print(a.table_state(0))


def test_neutral():  # ok
    table = [
        [0, 1, 3, 2],
        [0, 0, 0, 0],
        [0, 1, 2, 3],
        [0, 1, 1, 2]
    ]
    print(left_neutral(table, 4))  # ok
    table = [
        [0, 0, 0, 2],
        [0, 1, 1, 0],
        [0, 1, 2, 3],
        [0, 1, 3, 2]
    ]
    print(right_neutral(table, 4))  # ok


def test_distributivity():
    table1 = [
        [],
        []
    ]
    table2 = [
        [],
        []
    ]


def test_inverse():
    table1 = [
        [],
        []
    ]
    table2 = [
        [],
        []
    ]


def test_absorption():
    table1 = [
        [],
        []
    ]
    table2 = [
        [],
        []
    ]


def test_contractility():
    table = [
        [],
        [],
        [],
        []
    ]


def test_solvability():
    table = [
        [],
        [],
        [],
        []
    ]


def test_structure_table_properties_check():
    table = [
        [],
        [],
        [],
        []
    ]
    print(table_properties_check(table, 4))


def test_structure_sw_table_state():
    pass


def test_structure_sw_pair_tables_check():
    pass


def test_structure_sw_structure_state():
    table1 = [
        [0, 1, 2],
        [2, 1, 0],
        [2, 2, 2]
    ]
    table2 = [
        [0, 0, 0],
        [1, 0, 2],
        [1, 1, 2]
    ]
    table3 = [
        [1, 1, 0],
        [2, 2, 1],
        [0, 1, 0]
    ]
    a = SW(table1, table2, table3, table1, table2)
    print(a)
    # print(a.table_state(0))
    a_tables_properties = a.structure_state()
    for prop in a_tables_properties:
        print(prop)


def test_structure_check_structure_with_one_op():  # ok
    table = [
        [0, 0, 0, 2],
        [0, 1, 1, 0],
        [0, 1, 2, 3],
        [0, 1, 3, 2]
    ]
    table2 = [
        [0, 1, 2, 3],
        [1, 2, 3, 0],
        [2, 3, 0, 1],
        [3, 0, 1, 2]
    ]
    table3 = [
        [0, 1, 3, 2],
        [3, 2, 1, 0],
        [2, 3, 0, 1],
        [1, 0, 2, 3]
    ]
    print(check_structure_with_one_operation(table, 4))
    print(check_structure_with_one_operation(table2, 4))
    print(check_structure_with_one_operation(table3, 4))


def test_structure_check_structure_with_one_op2():  # ok
    table = [
        [0, 0, 0, 2],
        [0, 1, 1, 0],
        [0, 1, 2, 3],
        [0, 1, 3, 2]
    ]
    table2 = [
        [0, 1, 2, 3],
        [1, 2, 3, 0],
        [2, 3, 0, 1],
        [3, 0, 1, 2]
    ]
    table3 = [
        [0, 1, 3, 2],
        [3, 2, 1, 0],
        [2, 3, 0, 1],
        [1, 0, 2, 3]
    ]
    print(check_structure_with_one_operation(table, 4))
    print(check_structure_with_one_operation(table2, 4))
    print(check_structure_with_one_operation(table3, 4))


def test_structure_check_structure_with_two_ops():  # field ok
    table2 = [
        [0, 1, 2, 3],
        [1, 0, 3, 2],
        [2, 3, 0, 1],
        [3, 2, 1, 0]
    ]
    table3 = [
        [0, 0, 0, 0],
        [0, 1, 2, 3],
        [0, 2, 3, 1],
        [0, 3, 1, 2]
    ]
    print()
    print(check_structure_with_one_operation(table2, 4))
    print(check_structure_with_one_operation(table3, 4))

    # print(check_structure_with_one_operation2(table2, 4))
    # print(check_structure_with_one_operation2(table3, 4))
    print('--'*30)
    print(check_structure_with_two_operations(table2, table3, 4))


def test_md_non_isomorf_gen():
    k = int(input())
    nums = 0
    try:
        for num in md.generate_non_isomorf_nums_fixed(k):
            print(num)
            nums += 1
    except KeyboardInterrupt:
        print('прервано', num)
    print('fixed', nums)

    nums = 0
    try:
        for num in md.generate_non_isomorf_nums(k):
            print(num)
            nums += 1
    except KeyboardInterrupt:
        print('прервано', num)
    print('old', nums)
    # print(len(nums))


def main():
    # test_class_init_and_display()
    # test_structure_sw_structure_state()
    # test_structure_check_structure_with_one_op()
    # test_structure_check_structure_with_one_op2()
    # test_structure_check_structure_with_two_ops()
    # test_neutral()
    test_md_non_isomorf_gen()


if __name__ == "__main__":
    main()
