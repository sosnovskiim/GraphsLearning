import os
from graph import Graph


class GraphApp:
    def __init__(self):
        self.graphs = {}
        self.current = None

    def run(self):
        self.__print_help()
        while True:
            try:
                command = input("\n> ").strip().lower()
                if not command:
                    continue
                if command == "create":
                    self.__create_graph()
                elif command == "copy":
                    self.__copy_graph()
                elif command == "load":
                    self.__load_graph()
                elif command == "save":
                    self.__save_graph()
                elif command == "delete":
                    self.__delete_graph()
                elif command == "list":
                    self.__show_graphs()
                elif command == "switch":
                    self.__switch_graph()
                elif command == "info":
                    self.__show_info()
                elif command == "show":
                    self.__show_graph()
                elif command == "addv":
                    self.__add_vertex()
                elif command == "adde":
                    self.__add_edge()
                elif command == "delv":
                    self.__remove_vertex()
                elif command == "dele":
                    self.__remove_edge()
                elif command == "help":
                    self.__print_help()
                elif command == "exit":
                    print("Выход из программы")
                    break
                elif command == "outn":
                    self.__get_out_neighbors()
                elif command == "outdg":
                    self.__get_vertexes_with_greater_out_degree()
                else:
                    print("Ошибка: неизвестная команда, введите 'help' для просмотра доступных команд")
            except Exception as e:
                print(e)

    def __check_current(self):
        if self.current is None:
            raise ValueError("Ошибка: нет текущего графа, создайте или загрузите его")

    def __create_graph(self):
        name = input("Введите имя нового графа: ").strip()
        if not name:
            print("Ошибка: имя графа не может быть пустым")
            return
        if name in self.graphs:
            print("Ошибка: граф с таким именем уже существует")
            return

        directed_str = input("Ориентированный? (Y/n): ").strip().lower()
        directed = directed_str == "y"
        weighted_str = input("Взвешенный? (Y/n): ").strip().lower()
        weighted = weighted_str == "y"

        self.graphs[name] = Graph(directed, weighted)
        self.current = name
        print(f"Граф '{name}' создан и выбран как текущий")

    def __copy_graph(self):
        self.__check_current()
        name = input("Введите имя графа для копирования: ").strip()
        if name not in self.graphs:
            print("Ошибка: граф с таким именем не найден")
            return

        new_name = input("Введите имя нового графа: ").strip()
        if not new_name:
            print("Ошибка: имя графа не может быть пустым")
            return
        if new_name in self.graphs:
            print("Ошибка: граф с таким именем уже существует")
            return

        self.graphs[new_name] = Graph.copy(self.graphs[name])
        self.current = new_name
        print(f"Граф '{name}' скопирован в '{new_name}' и выбран как текущий")

    def __load_graph(self):
        filename = input("Имя файла для загрузки: ").strip()
        if not os.path.exists(filename):
            print("Ошибка: файл не найден")
            return
        try:
            graph = Graph.get_from_file(filename)
        except Exception as e:
            print(e)
            return

        name = input("Введите имя для этого графа: ").strip()
        if not name:
            name = os.path.splitext(os.path.basename(filename))[0]
        if name in self.graphs:
            print("Ошибка: граф с таким именем уже существует")
            return

        self.graphs[name] = graph
        self.current = name
        print(f"Граф '{name}' загружен и выбран как текущий")

    def __save_graph(self):
        self.__check_current()
        filename = input("Имя файла для сохранения: ").strip()
        if not filename:
            print("Ошибка: имя файла не может быть пустым")
            return
        try:
            self.graphs[self.current].save_to_file(filename)
            print(f"Текущий граф сохранён в {filename}")
        except Exception as e:
            print(e)

    def __delete_graph(self):
        self.__check_current()
        name = input("Имя графа для удаления: ").strip()
        if not name:
            name = self.current
        if name not in self.graphs:
            print("Ошибка: граф с таким именем не найден")
            return
        del self.graphs[name]
        if name == self.current:
            self.current = next(iter(self.graphs)) if self.graphs else None
        print(f"Граф '{name}' удалён из памяти")

    def __show_graphs(self):
        self.__check_current()
        print("Список графов:")
        for name in sorted(self.graphs.keys()):
            is_current = "*" if name == self.current else "-"
            graph = self.graphs[name]
            directed_str = f"{"" if graph.directed else "не"}ор."
            weighted_str = f"{"" if graph.weighted else "не"}взв."
            vertexes_cnt = f"{len(graph.get_vertexes())} вершин"
            edges_cnt = f"{len(graph.get_edges())} рёбер"
            print(f"{is_current} {name} ({directed_str}, {weighted_str}, {vertexes_cnt}, {edges_cnt})")

    def __switch_graph(self):
        self.__check_current()
        name = input("Введите имя графа для переключения: ").strip()
        if name not in self.graphs:
            print("Ошибка: граф с таким именем не найден")
            return
        self.current = name
        print(f"Текущий граф: {name}")

    def __show_info(self):
        self.__check_current()
        graph = self.graphs[self.current]
        print(f"Граф '{self.current}':")
        print(f"- Ориентированный: {"да" if graph.directed else "нет"}")
        print(f"- Взвешенный: {"да" if graph.weighted else "нет"}")
        print(f"- Количество вершин: {len(graph.get_vertexes())}")
        print(f"- Количество рёбер: {len(graph.get_edges())}")

    def __show_graph(self):
        self.__check_current()
        print(self.graphs[self.current])

    def __add_vertex(self):
        self.__check_current()
        v = input("Имя новой вершины: ").strip()
        if not v:
            print("Ошибка: имя вершины не может быть пустым")
            return
        try:
            self.graphs[self.current].add_vertex(v)
            print(f"Вершина '{v}' добавлена")
        except ValueError as e:
            print(e)

    def __add_edge(self):
        self.__check_current()
        g = self.graphs[self.current]
        u = input("Первая вершина: ").strip()
        v = input("Вторая вершина: ").strip()
        if g.weighted:
            w_str = input("Вес ребра: ").strip()
            try:
                w = int(w_str)
            except ValueError:
                print("Ошибка: вес ребра должен быть числом")
                return
            try:
                g.add_edge(u, v, w)
                print(f"Ребро '{u}' -> '{v}' весом {w} добавлено")
            except ValueError as e:
                print(e)
        else:
            try:
                g.add_edge(u, v)
                print(f"Ребро '{u}' -> '{v}' добавлено")
            except ValueError as e:
                print(e)

    def __remove_vertex(self):
        self.__check_current()
        v = input("Имя вершины для удаления: ").strip()
        try:
            self.graphs[self.current].remove_vertex(v)
            print(f"Вершина '{v}' удалена")
        except ValueError as e:
            print(e)

    def __remove_edge(self):
        self.__check_current()
        u = input("Первая вершина: ").strip()
        v = input("Вторая вершина: ").strip()
        try:
            self.graphs[self.current].remove_edge(u, v)
            print(f"Ребро '{u}' -> '{v}' удалено")
        except ValueError as e:
            print(e)

    def __get_out_neighbors(self):
        self.__check_current()
        v = input("Вершина: ").strip()
        neighbors = self.graphs[self.current].get_out_neighbors(v)
        if not neighbors:
            print(f"Вершина '{v}' не имеет исходящих соседних вершин")
        else:
            graph = self.graphs[self.current]
            if graph.weighted:
                neighbors_str = ", ".join(f"{n} ({w})" for n, w in neighbors.items())
            else:
                neighbors_str = ", ".join(neighbors.keys())
            print(f"Исходящие соседние вершины '{v}': {neighbors_str}")

    def __get_vertexes_with_greater_out_degree(self):
        self.__check_current()
        v = input("Вершина: ").strip()
        graph = self.graphs[self.current]
        result = graph.get_vertexes_with_greater_out_degree(v)
        if not result:
            print(f"Нет вершин с полустепенью исхода больше, чем у '{v}'")
        else:
            print(f"Вершины с полустепенью исхода больше, чем у '{v}':")
            print(", ".join([f"{u} ({degree})" for u, degree in result]))

    @staticmethod
    def __print_help():
        print("""
Доступные команды:
- create - создать новый граф
- copy   - скопировать имеющийся граф
- load   - загрузить граф из файла
- save   - сохранить текущий граф в файл
- delete - удалить граф из памяти
- list   - показать список всех графов в памяти
- switch - переключиться на другой граф
- info   - информация о текущем графе
- show   - показать список смежности текущего графа
- addv   - добавить вершину в текущий граф
- adde   - добавить ребро в текущий граф
- delv   - удалить вершину из текущего графа
- dele   - удалить ребро из текущего графа
- help   - показать доступные команды
- exit   - выход из программы
  
Дополнительные команды:
- outn  - показать все исходящие соседние вершины заданной
- outdg - показать вершины с полустепенью исхода больше, чем у заданной
        """)


if __name__ == "__main__":
    app = GraphApp()
    app.run()
