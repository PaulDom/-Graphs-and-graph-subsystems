from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel


def convert():
    # считываем с виджета и заносим в двумерный список(матрица)
    adj_matrix_str = adj_matrix_input.toPlainText()
    adj_matrix = []
    for row in adj_matrix_str.split('\n'):
        if row:
            adj_matrix.append(list(map(int, row.split())))

    # получаем матрицы инцидентов на основе матрицы смежностей
    inc_matrix_res = inc_matrix(adj_matrix)
    int_matrix_right_res = inc_matrix_right(adj_matrix)

    # преобразование матрицы инцидентов в строку
    matrix_to_str = ''
    for row in inc_matrix_res:
        line = ' '.join(f'{elem:2}' for elem in row)
        matrix_to_str += line + '\n'


    # строку матрицы инцидетов вставляем в виджет для вывода
    inc_matrix_output.setPlainText(matrix_to_str)

    # преобразование множества правых инцидентов в строку
    result = []
    for item in int_matrix_right_res:
        vertex = item[0]  # Номер вершины
        neighbors = item[1]  # Список смежных вершин
        result.append(f"{vertex}:{neighbors}")

    matrix_right_to_str = "\n".join(result)

    # строку множества правых инцидентов вставляем в виджет для вывода
    right_inc_set_output.setPlainText(matrix_right_to_str)

def inc_matrix(adj_matrix):
    edges = []

    # Определяем рёбра (ориентируем от меньшего индекса к большему)
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix)):
            if adj_matrix[i][j] == 1:  # Ориентированный граф
                edges.append((i, j))

    # Создаём пустую матрицу инцидентности (строки - вершины, столбцы - рёбра)
    inc_matrix_res = []
    for i in range(len(adj_matrix)):
        row = []
        for j in range(len(edges)):
            row.append(0)
        inc_matrix_res.append(row)

    # Заполняем матрицу инцидентности
    for edge_idx, (v1, v2) in enumerate(edges):
        inc_matrix_res[v1][edge_idx] = -1  # Начальная вершина
        inc_matrix_res[v2][edge_idx] = 1  # Конечная вершина

    return inc_matrix_res

def inc_matrix_right(adj_matrix):
    right_incidents = []  # Инициализируем пустой список для результата

    for i, row in enumerate(adj_matrix):
        # Инициализируем список для текущей вершины
        incidents = []

        # Проходим по каждому значению строки
        for j, value in enumerate(row):
            if value == 1:  # Если существует ребро из вершины i в j
                incidents.append(j + 1)  # Добавляем вершину в список

        # Добавляем текущую вершину и её инцидентные вершины в общий список
        right_incidents.append([i + 1, incidents])

    return right_incidents


app = QApplication([])
main_win = QWidget()

layout = QVBoxLayout()

adj_matrix_label = QLabel('Введите матрицу смежности (через пробелы и новые строки):')
layout.addWidget(adj_matrix_label)

adj_matrix_input = QTextEdit()
layout.addWidget(adj_matrix_input)

convert_button = QPushButton('Преобразовать')
convert_button.clicked.connect(convert)
layout.addWidget(convert_button)

inc_matrix_label = QLabel('Матрица инцидентности:')
layout.addWidget(inc_matrix_label)

inc_matrix_output = QTextEdit()
inc_matrix_output.setReadOnly(True)
layout.addWidget(inc_matrix_output)

right_inc_set_label = QLabel('Множество правых инцидентностей:')
layout.addWidget(right_inc_set_label)

right_inc_set_output = QTextEdit()
right_inc_set_output.setReadOnly(True)
layout.addWidget(right_inc_set_output)

main_win.setLayout(layout)
main_win.setWindowTitle('Преобразование матриц')
main_win.show()


app.exec_()
'''
0 1 0 1
0 0 1 0
0 0 0 1
0 0 0 0

0 0 1 1 0
1 0 0 1 0
1 1 0 1 0
0 0 0 0 0
1 0 0 0 0
'''