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
                elif command == "symd":
                    self.__get_symmetric_difference()
                elif command == "allp":
                    self.__get_all_paths_between()
                elif command == "mind":
                    self.__get_shortest_distances_to()
                elif command == "mst":
                    self.__get_kruskal_mst()
                elif command == "spb":
                    self.__get_shortest_path_floyd()
                elif command == "spf":
                    self.__get_shortest_paths_bellman_ford()
                elif command == "allsp":
                    self.__get_all_shortest_paths_dijkstra()
                elif command == "flow":
                    self.__get_max_flow()
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
        graph = self.graphs[self.current]
        directed_str = f"{"" if graph.directed else "не"}ориентированный"
        weighted_str = f"{"" if graph.weighted else "не"}взвешенный"
        print(f"Граф '{self.current}': {directed_str}, {weighted_str}")
        print(graph)

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

    def __get_symmetric_difference(self):
        self.__check_current()
        if len(self.graphs) < 2:
            print("Ошибка: для выполнения операции нужно хотя бы два графа")
            return

        name1 = input("Введите имя первого графа: ").strip()
        name2 = input("Введите имя второго графа: ").strip()
        if name1 not in self.graphs or name2 not in self.graphs:
            print("Ошибка: оба графа должны существовать")
            return

        graph1 = self.graphs[name1]
        graph2 = self.graphs[name2]
        try:
            graph3 = graph1.get_symmetric_difference(graph2)
        except ValueError as e:
            print(e)
            return

        name3 = input("Введите имя нового графа: ").strip()
        if not name3:
            print("Ошибка: имя графа не может быть пустым")
            return
        if name3 in self.graphs:
            print("Ошибка: граф с таким именем уже существует")
            return
        self.graphs[name3] = graph3
        self.current = name3
        print(f"Симметрическая разность '{name3}' создана и выбрана как текущий граф")

    def __get_all_paths_between(self):
        self.__check_current()
        u = input("Начальная вершина: ").strip()
        v = input("Конечная вершина: ").strip()
        try:
            graph = self.graphs[self.current]
            paths = graph.get_all_paths_between(u, v)
            if not paths:
                print(f"Нет ни одного пути из '{u}' в '{v}'")
            else:
                print(f"Найдено {len(paths)} путей из '{u}' в '{v}':")
                for i, path in enumerate(paths, 1):
                    print(f"{i}: {' -> '.join(path)}")
        except ValueError as e:
            print(e)

    def __get_shortest_distances_to(self):
        self.__check_current()
        v = input("Целевая вершина: ").strip()
        try:
            graph = self.graphs[self.current]
            distances = graph.get_shortest_distances_to(v)
            print(f"Кратчайшие расстояния (по числу дуг) до вершины '{v}':")
            for v in sorted(graph.get_vertexes()):
                if v in distances:
                    print(f"{v}: {distances[v]}")
                else:
                    print(f"{v}: ...")
        except ValueError as e:
            print(e)

    def __get_kruskal_mst(self):
        self.__check_current()
        graph = self.graphs[self.current]
        try:
            mst = graph.get_kruskal_mst()
        except ValueError as e:
            print(e)
            return

        name = input("Введите имя нового графа: ").strip()
        if not name:
            print("Ошибка: имя графа не может быть пустым")
            return
        if name in self.graphs:
            print("Ошибка: граф с таким именем уже существует")
            return

        self.graphs[name] = mst
        self.current = name
        print(f"Минимальное остовное дерево '{name}' создано и выбрано как текущий граф")

    # def __get_shortest_path_bellman_ford(self):
    #     self.__check_current()
    #     u = input("Начальная вершина: ").strip()
    #     v = input("Конечная вершина: ").strip()
    #     try:
    #         g = self.graphs[self.current]
    #         distance, parent = g.get_shortest_path_bellman_ford(u, v)
    #         if distance == float("inf"):
    #             print(f"Нет ни одного пути из '{u}' в '{v}'")
    #         else:
    #             path = g.restore_path_from_parent(parent, v)
    #             print(f"Кратчайшее расстояние от '{u}' до '{v}': {distance}")
    #             print("Путь:", " -> ".join(path))
    #     except ValueError as e:
    #         print(e)
    #
    # def __get_shortest_paths_dijkstra(self):
    #     self.__check_current()
    #     u = input("Начальная вершина: ").strip()
    #     try:
    #         g = self.graphs[self.current]
    #         distance, parent = g.get_shortest_paths_dijkstra(u)
    #         print(f"Кратчайшие расстояния от вершины '{u}':")
    #         for v in sorted(distance.keys()):
    #             if distance[v] == float("inf"):
    #                 print(f"{v}: ...")
    #             else:
    #                 path = g.restore_path_from_parent(parent, v)
    #                 print(f"{v}: {distance[v]} ({" -> ".join(path)})")
    #     except ValueError as e:
    #         print(e)
    #
    # def __get_all_shortest_paths_floyd(self):
    #     self.__check_current()
    #     g = self.graphs[self.current]
    #     try:
    #         distances, next = g.get_all_shortest_paths_floyd()
    #         vertexes = sorted(g.get_vertexes())
    #         print("Кратчайшие расстояния между всеми парами вершин:")
    #         for u in vertexes:
    #             for v in vertexes:
    #                 if u == v:
    #                     continue
    #                 d = distances[u][v]
    #                 if d == float("inf"):
    #                     print(f"{u} -> {v}: ...")
    #                 else:
    #                     path = g.restore_path_floyd(next, u, v)
    #                     print(f"{u} -> {v}: {d} ({" -> ".join(path)})")
    #     except ValueError as e:
    #         print(e)

    def __get_shortest_path_floyd(self):
        self.__check_current()
        u = input("Начальная вершина: ").strip()
        v = input("Конечная вершина: ").strip()
        try:
            g = self.graphs[self.current]
            dist, next = g.get_shortest_path_floyd(u, v)
            if dist == float("inf"):
                print(f"Нет ни одного пути из '{u}' в '{v}'")
            else:
                path = g.restore_path_floyd(next, u, v)
                print(f"Кратчайшее расстояние от '{u}' до '{v}': {dist}")
                print("Путь:", " -> ".join(path))
        except ValueError as e:
            print(e)

    def __get_shortest_paths_bellman_ford(self):
        self.__check_current()
        u = input("Начальная вершина: ").strip()
        try:
            g = self.graphs[self.current]
            dist, parent = g.get_shortest_paths_bellman_ford(u)
            print(f"Кратчайшие расстояния от вершины '{u}':")
            for v in sorted(dist.keys()):
                if dist[v] == float("inf"):
                    print(f"{v}: ...")
                else:
                    path = g.restore_path_from_parent(parent, v)
                    print(f"{v}: {dist[v]} ({" -> ".join(path)})")
        except ValueError as e:
            print(e)

    def __get_all_shortest_paths_dijkstra(self):
        self.__check_current()
        try:
            g = self.graphs[self.current]
            all_dist, all_parent = g.get_all_shortest_paths_dijkstra()
            vertexes = sorted(g.get_vertexes())
            print("Кратчайшие расстояния между всеми парами вершин:")
            for u in vertexes:
                for v in vertexes:
                    if u == v:
                        continue
                    d = all_dist[u][v]
                    if d == float("inf"):
                        print(f"{u} -> {v}: ...")
                    else:
                        path = g.restore_path_from_parent(all_parent[u], v)
                        print(f"{u} -> {v}: {d} ({" -> ".join(path)})")
        except ValueError as e:
            print(e)

    def __get_max_flow(self):
        self.__check_current()
        g = self.graphs[self.current]
        source = input("Источник: ").strip()
        sink = input("Сток: ").strip()
        try:
            flow = g.get_max_flow(source, sink)
            print(f"Максимальный поток из '{source}' в '{sink}': {flow}")
        except ValueError as e:
            print(e)

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
- symd  - построить симметрическую разность двух орграфов
- allp  - вывести все пути из одной вершины в другую
- mind  - вывести длины кратчайших путей от всех вершин до заданной
- mst   - построить минимальное остовное дерево методом Краскала
- spb   - кратчайший путь из одной вершины в другую
- spf   - кратчайшие пути из одной вершины во все остальные
- allsp - кратчайшие пути между всеми парами вершин
- flow  - максимальный поток от источника к стоку
        """)


if __name__ == "__main__":
    app = GraphApp()
    app.run()
