from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QMessageBox

def to_string():
    input_text_str = input_text.toPlainText()
    result_dict = {}

    lines = input_text_str.split('\n')

    for line in lines:
        if ':' in line:
            key, value = line.split(':')
            key = key.strip()
            # Convert the value to a list of integers
            value = value.strip()[1:-1].split(',')
            value = [int(v) for v in value if v]
            # Add the key-value pair to the dictionary
            result_dict[int(key)] = value

    return result_dict

def start_process():
    data = to_string()

    res = kosaraju(data)
    input_subsystem(res)

    components = extract_vertices(res)

    inc_matrix = create_incidence_matrix(components, data)
    input_subsystem_ins_matrix(inc_matrix)

def kosaraju(graph):
    def dfs(v, visited, stack):
        visited.add(v)
        for neighbor in graph[v]:
            if neighbor not in visited:
                dfs(neighbor, visited, stack)
        stack.append(v)

    def reverse_graph(graph):
        reversed_graph = {key: [] for key in graph}
        for v, neighbors in graph.items():
            for neighbor in neighbors:
                reversed_graph[neighbor].append(v)
        return reversed_graph

    def fill_order(graph):
        visited = set()
        stack = []
        for v in graph:
            if v not in visited:
                dfs(v, visited, stack)
        return stack

    def dfs_assign(v, visited, component, reversed_graph):
        visited.add(v)
        component.append(v)
        for neighbor in reversed_graph[v]:
            if neighbor not in visited:
                dfs_assign(neighbor, visited, component, reversed_graph)

    def find_edges(component, original_graph):
        edges = []
        for v in component:
            for neighbor in original_graph[v]:
                if neighbor in component:
                    edges.append((neighbor, v))
        return edges

    stack = fill_order(graph)
    reversed_graph = reverse_graph(graph)
    visited = set()
    components = []

    while stack:
        v = stack.pop()
        if v not in visited:
            component = []
            dfs_assign(v, visited, component, reversed_graph)
            edges = find_edges(component, graph)
            components.append((component, edges))

    return components

def input_subsystem(components):
    output_text.clear()

    # Записываем компоненты в текстовом формате
    for i, component in enumerate(components, start=1):
        component_str = ", ".join(map(str, component))
        output_text.append(f"{i}: [{component_str}]")

def find_subsystem_index(vertex, subsystems):
    for i, subsystem in enumerate(subsystems):
        if vertex in subsystem:
            return i
    return None

def create_incidence_matrix(subsystems, left_incidence):
    edges = []

    # Определяем связи между подсистемами
    for vertex, neighbors in left_incidence.items():
        for neighbor in neighbors:
            subsystem_index = find_subsystem_index(vertex, subsystems)
            neighbor_subsystem_index = find_subsystem_index(neighbor, subsystems)
            if subsystem_index is not None and neighbor_subsystem_index is not None and subsystem_index != neighbor_subsystem_index:
                edges.append((neighbor_subsystem_index, subsystem_index))

    # Удаляем дублирующиеся ребра и сохраняем только уникальные
    unique_edges = list(set(edges))

    n = len(subsystems)
    m = len(unique_edges)
    matrix = [[0] * m for _ in range(n)]

    for j, (from_subsystem, to_subsystem) in enumerate(unique_edges):
        matrix[from_subsystem][j] = -1
        matrix[to_subsystem][j] = 1

    return matrix

def input_subsystem_ins_matrix(matrix):
    inc_matrix_text = '\n'.join([' '.join(map(str, row)) for row in matrix])
    matrix_text.setPlainText(inc_matrix_text)

def extract_vertices(components_with_edges):
    return [component[0] for component in components_with_edges]

app = QApplication([])

# Главное окно
main_window = QWidget()
main_window.setWindowTitle("Подграфы")
main_window.setGeometry(1000, 400, 600, 800)

main_layout = QVBoxLayout()

# Виджет ввода
input_label = QLabel("Введите множестве левых инцидентов")
input_text = QTextEdit()
process_but = QPushButton("Расчитать")
process_but.clicked.connect(start_process)
main_layout.addWidget(input_label)
main_layout.addWidget(input_text)
main_layout.addWidget(process_but)

# Виджет вывода подсистем
output_label = QLabel("Подсистемы:")
output_text = QTextEdit()
output_text.setReadOnly(True)
main_layout.addWidget(output_label)
main_layout.addWidget(output_text)

# Виджет вывода графа инциденций подсистем
matrix_label = QLabel("Граф инциденций подсистем")
matrix_text = QTextEdit()
matrix_text.setReadOnly(True)
main_layout.addWidget(matrix_label)
main_layout.addWidget(matrix_text)

main_window.setLayout(main_layout)
main_window.show()
app.exec_()