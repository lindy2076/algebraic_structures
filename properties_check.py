def associtiativity(table, n: int) -> bool:  # A1 - ассоциативность
    for x in range(n):
        for y in range(n):
            for z in range(n):
                if table[table[x][y]][z] != table[x][table[y][z]]:
                    return False
    return True


def commutativity(table, n: int) -> bool:  # A2 - коммутативность
    for i in range(n):
        for j in range(i, n):
            if table[i][j] != table[j][i]:
                return False
    return True


def left_distributivity(table1, table2, n: int) -> bool:  # A3_1 - дистрибутивность слева
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if table1[a][table2[b][c]] != table2[table1[a][b]][table1[a][c]]:
                    # print("не дистрибутивные элементы слева: ", a, b, c)
                    return False
    return True


def right_distributivity(table1, table2, n: int) -> bool:  # A3_2 - дистрибутивность справа
    elems = list(range(n))  # FIXME надо проверить как быстрее: сверху(дистр. слева) или тут
    for a in elems:
        for b in elems:
            for c in elems:
                if table1[table2[a][b]][c] != table2[table1[a][c]][table1[b][c]]:
                    # print("не дистрибутивные элементы справа: ", a, b, c)
                    return False
    return True


def left_absorption(table1, table2, n: int) -> bool:  # A4_1 - поглощение слева
    for a in range(n):
        for b in range(n):
            if table1[table2[a][b]][a] != a:
                return False
    return True


def right_absorption(table1, table2, n: int) -> bool:  # A4_2 - поглощение справа
    elems = list(range(n))
    for a in elems:
        for b in elems:
            if table1[a][table2[a][b]] != a:
                return False
    return True


def idempotence(table, n: int) -> bool:  # A5 - идемпотентность
    for i in range(n):
        if table[i][i] != i:
            return False
    return True


def left_neutral(table, n: int) -> int:  # A6_1 - левый нейтральный
    """
    возвращает нейтральный элемент; -1, если нет нейтрального
    """
    elems = list(range(n))
    for i, line in enumerate(table):
        if line == elems:
            return i
    return -1


def right_neutral(table, n: int) -> int:  # A6_2 - правый нейтральный
    """
    возвращает нейтральный элемент; -1, если нет нейтрального
    """
    elems = list(range(n))
    column = []
    for i in elems:
        for j in elems:
            column.append(table[j][i])
        if column == elems:
            return i
        column = []
    return -1


def left_contractility(table, n: int) -> bool:  # A7_1 - левая сократимость (2.1.5.4)
    string_set = set()
    for i in range(n):
        for j in range(n):
            if table[i][j] in string_set:
                return False
            else:
                string_set.add(table[i][j])
        string_set = set()
    return True


def right_contractility(table, n: int) -> bool:  # A7_2 - правая сократимость
    column_set = set()
    for j in range(n):
        for i in range(n):
            if table[i][j] in column_set:
                return False
            else:
                column_set.add(table[i][j])
        column_set = set()
    return True


def left_inverse(table, n: int, neutral: int = None) -> bool:  # A8_1 левый обратный
    if neutral is None:
        print("[нет нейтрального]", end=" ")
        return False
    for i in range(n):
        flag = False
        for j in range(n):
            if table[j][i] == neutral:
                flag = True  # есть нейтральный в столбце
                break
        if not flag:
            return False
    return True


def right_inverse(table, n: int, neutral: int = None) -> bool:  # A8_1 правый обратный
    if neutral is None:
        print("[нет нейтрального]", end=" ")
        return False
    for i in range(n):
        flag = False
        for j in range(n):
            if table[i][j] == neutral:
                flag = True  # есть нейтральный в строке
                break
        if not flag:
            return False
    return True


def solvability(table, n: int) -> bool:  # A9 - разрешимость (2.1.5.5)
    column_set = set()
    for i in range(n):
        if set(table[i]) != set(range(n)):
            return False
        for j in range(n):
            if table[j][i] in column_set:
                return False
            else:
                column_set.add(table[j][i])
        column_set = set()
    return True
