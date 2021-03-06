# что это 

Программа создана в рамках студенческой лаборатории для обнаружения бинарных операций, образующих известные(мне) алгебраические структуры.

Для решения этой задачи я решил написать небольшое консольное приложение на python с расширенным функционалом.

# что можно делать 

- вводить свою таблицу Кэли операции, проверять её свойства и выявлять образованную ею алгебраическую структуру
- добавлять таблицы в память и проверять уже две таблицы на задание алгебраической структуры
- генерировать все неизоморфные таблицы Кэли для двух- и трёхэлементных множеств и проверять, какие алгебраические структуры они образуют попарно и по отдельности


# что нужно

- python
- colorama

# команды 

- help/h - выводит список команд 

- num/n *string* - выводит номер, кодирующий таблицу, введённую в строку пользователем через пробелы.   
  
  ![num eg](https://user-images.githubusercontent.com/67479681/170885387-858d5362-786d-4be3-b301-2863a9b1ac86.png)

- print/p *set_len table_num* - вывод таблицы, закодированной числом table_num, и заданной на set_len-элементном множестве. 
  
  ![print eg](https://user-images.githubusercontent.com/67479681/170885407-e20d0300-6fdd-4ee5-adcd-49ad775e9251.png)

- solo *n* - вывод списка типов алгебраических структур с одной операцией, заданных всеми неизоморфными таблицами на n-элементном множестве. 

  ![solo eg](https://user-images.githubusercontent.com/67479681/170885428-8eedaa79-641c-44b4-b42e-38c1e6868528.png)

- double *n* - вывод списка типов алгебраических структур с двумя операциями, заданных всеми неизоморфными таблицами на n-элементном множестве.

- type/t *set_len, table_num* - пишет свойства таблицы номер table_num и тип алгебраической структуры  

  ![type eg](https://user-images.githubusercontent.com/67479681/170885558-0db3d2e5-ea3e-413b-9377-ca6f6e7c885b.png)

- temp - вывод таблиц из памяти программы 

  Память программы содержит добавленные в неё пользователем таблицы. В памяти таблицы пронумерованы и имеют свои индексы в памяти. 

- add *set_len table_num* - добавляет таблицу под кодом table_num в память 

- del *index* - удаляет таблицу под индексом index из памяти 

- mix *index1 index2* - вывод типов структур, образованных таблицами из памяти под индексами index1 и index2 

  ![mix eg](https://user-images.githubusercontent.com/67479681/170885614-b42fa45d-dd26-4420-ae3a-2f1e3f375fca.png)

- info - выводит информацию о программе 

- q - выйти из программы 

# контекст 🤓

 Бинарной операцией на конечном множестве называется функция от двух переменных, заданная из декартова квадрата множества в само множество. 
 То есть, если поместить в функцию два элемента множества, то она выдаст элемент множества. 
 Так как результат операции зависит от двух переменных, то её можно задать с помощью квадратной матрицы, строки и столбцы которой помечены элементами множества.
 Результат операции лежит в ячейке на пересечении строки, помеченной первой переменной, и столбца, помеченного второй переменной. 
 На рисунке приведён пример таблицы Кэли, для которой справедливо a * a = a, a * b = a. 
 
 ![пример](https://user-images.githubusercontent.com/67479681/170885268-a9bf2527-33f9-4cc4-ab49-aef5f433e406.png)

 
 Бинарная операция обладает некими свойствами, и некоторые встречаются довольно часто. Мы будем рассматривать 9 свойств, обозначенные A1, A2, A3, …, A9 

- A1: ассоциативность: a * (b * c) = (a * b) * c для всех a, b, c 

- A2: коммутативность: a * b = b * a для всех a, b 

- A3: дистрибутивность операции ‘*’ относительно операции ‘+’: 

  - А3_1: слева: a * (b + c) = (a * b) + (a * c) для всех a, b, c 
  - A3_2: справа (a + b) * c = (a * c) + (b * c) для всех a, b, c 

- А4: поглощение операции ‘*’ операцией ‘+’: 
  - А4_1: слева: a * (a + b) = a для всех a, b 

  - A4_1: справа: (a + b) * a = a для всех a, b 

- А5: идемпотентность: a * a = a для всех a 

- A6: наличие нейтрального 
  - A6_1: левого: существует такой e, что e * a = a для всех a 

  - A6_2: правого: существует такой e, что a * e = a для всех a 

- А7: сократимость 

  - А7_1: слева: из a * x и a * y следует x = y 

  - A7_2: справа: из x * a и y * a следует x = y 

- А8: наличие обратного к нейтральному элементу e (есть левый и правый) 

  - А8_1: слева: существует -a такой, что -a * a = e для всех а 

  - А8_2: справа: существует -a такой, что a * -a = e для всех a 

- А9: разрешимость: существуют единственные x, y такие, что a * x = y * a = b для всех a, b 


Изоморфными таблицами Кэли я называю такие таблицы, которые получаются перестановкой i-ой и j-ой строк и столбцов одновременно 
или последовательным применением таких перестановок. На рисунке ниже показан процесс перестановки 1 и 3 столбцов и строк таблицы. 

![перестановка](https://user-images.githubusercontent.com/67479681/170885317-8326fc4d-866d-4c3d-8523-408d5ca7faca.png)

----
❗
__Все таблицы рассматриваются на множестве неотрицательных целых чисел, меньших размера множества (list(range(set_len)).__
Если есть необходимость проверить на другом множестве, то надо просто переразметить таблицу, а именно переименовать переменные. 

❗**Все таблицы кодируются числом и длиной множества. Таблица представляется в виде строки так, чтобы каждая последующая строка таблицы приписывалась справа. 
Затем число из строки переводится в десятичную систему счисления.**

Программа различает следующие типы структур с одной операцией: 

Полугруппа (semigroup), обратимая полугруппа (reverse semigroup), группа (group), абелева группа (abel group), моноид (monoid), квазигруппа (quasigroup),
лупа(петля)((loop)), унитарная магма (unitar magma). 

![alg pic](https://user-images.githubusercontent.com/67479681/170885115-d9d0eaa4-b042-4554-9854-433238c53b57.PNG)
(на картинке обратимость = сократимость (А9) в наших терминах)

Для каждой структуры в назавние добавляется idem и commutative, если они обладают соответствующими свойствами (идемпотентности и коммутативности).
В случае абелевой группы commutative не добавляется. 

Абелева группа и полугруппа образуют кольцо (ring), абелева группа и моноид образуют кольцо с единицей (ring with neutral),
абелева группа и группа без нейтрального первой операции образуют тело (division ring),
а абелева группа и абелева группа без нейтрального первой операции образуют поле (field). Причём вторая операция должна быть дистрибутивна относительно первой.
