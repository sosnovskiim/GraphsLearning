import heapq
from collections import defaultdict, deque


class Graph:
    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted
        self.adjacency = {}

    @classmethod
    def get_from_file(cls, filename):
        with open(filename, "r", encoding="utf-8") as file_in:
            line = file_in.readline().strip()
            if not line:
                raise ValueError("Ошибка: файл пуст")

            parts = line.split()
            if len(parts) != 2:
                raise ValueError("Ошибка: первая строка должна содержать два числа: directed и weighted")
            directed = bool(int(parts[0]))
            weighted = bool(int(parts[1]))
            graph = cls(directed, weighted)

            line = file_in.readline().strip()
            if line:
                vertexes = line.split()
                for v in vertexes:
                    graph.add_vertex(v)

            for line in file_in:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if weighted:
                    if len(parts) < 3:
                        raise ValueError("Ошибка: во взвешенном графе ребро должно содержать вершину1, вершину2 и вес")
                    u, v, w = parts[0], parts[1], int(parts[2])
                    graph.add_edge(u, v, w)
                else:
                    if len(parts) < 2:
                        raise ValueError("Ошибка: в невзвешенном графе ребро должно содержать вершину1 и вершину2")
                    u, v = parts[0], parts[1]
                    graph.add_edge(u, v)
        return graph

    @classmethod
    def copy(cls, other):
        graph = cls(other.directed, other.weighted)
        for v, neighbors in other.adjacency.items():
            graph.adjacency[v] = neighbors.copy()
        return graph

    def add_vertex(self, v):
        if v in self.adjacency:
            raise ValueError(f"Ошибка: вершина '{v}' уже существует")
        self.adjacency[v] = {}

    def add_edge(self, u, v, weight=None):
        if u not in self.adjacency or v not in self.adjacency:
            raise ValueError("Ошибка: обе вершины должны существовать")

        if self.weighted:
            if weight is None:
                raise ValueError("Ошибка: для взвешенного графа необходимо указать вес")
            weight = int(weight)
        else:
            weight = 1

        if v in self.adjacency[u]:
            raise ValueError(f"Ошибка: ребро '{u}' -> '{v}' уже существует")

        self.adjacency[u][v] = weight
        if not self.directed:
            self.adjacency[v][u] = weight

    def remove_vertex(self, v):
        if v not in self.adjacency:
            raise ValueError(f"Ошибка: вершина '{v}' не существует")

        for u in list(self.adjacency.keys()):
            if v in self.adjacency[u]:
                del self.adjacency[u][v]
        del self.adjacency[v]

    def remove_edge(self, u, v):
        if u not in self.adjacency or v not in self.adjacency:
            raise ValueError("Ошибка: обе вершины должны существовать")

        if v not in self.adjacency[u]:
            raise ValueError(f"Ошибка: ребро '{u}' -> '{v}' не существует")

        del self.adjacency[u][v]
        if not self.directed:
            del self.adjacency[v][u]

    def get_vertexes(self):
        return list(self.adjacency.keys())

    def get_edges(self):
        edges = []
        for u in self.adjacency:
            for v, w in self.adjacency[u].items():
                if self.directed:
                    edges.append((u, v, w))
                elif u <= v:
                    edges.append((u, v, w))
        return edges

    def get_out_neighbors(self, v):
        if not self.directed:
            raise ValueError(f"Ошибка: текущий граф неориентированный")
        if v not in self.adjacency:
            raise ValueError(f"Ошибка: вершина '{v}' не существует")
        return self.adjacency[v].copy()

    def get_out_degree(self, v):
        return len(self.get_out_neighbors(v))

    def get_vertexes_with_greater_out_degree(self, v):
        if not self.directed:
            raise ValueError(f"Ошибка: текущий граф неориентированный")
        if v not in self.adjacency:
            raise ValueError(f"Ошибка: вершина '{v}' не существует")
        result = []
        for u, neighbors in self.adjacency.items():
            degree = len(neighbors)
            if degree > len(self.adjacency[v]):
                result.append((u, degree))
        return result

    def get_symmetric_difference(self, other):
        if not self.directed or not other.directed:
            raise ValueError("Ошибка: симметрическая разность определена только для орграфов")

        result = Graph(directed=True, weighted=False)
        vertexes = set(self.adjacency.keys()) | set(other.adjacency.keys())
        for v in vertexes:
            result.add_vertex(v)

        for u in vertexes:
            for v in vertexes:
                if u not in self.adjacency or u not in other.adjacency:
                    continue
                if (v in self.adjacency[u]) != (v in other.adjacency[u]):
                    result.add_edge(u, v)

        return result

    def __dfs(self, curr, end, path, visited):
        path = path + [curr]
        if curr == end:
            return [path]
        paths = []
        for neighbor in self.adjacency[curr]:
            if neighbor not in visited:
                new_paths = self.__dfs(neighbor, end, path, visited | {neighbor})
                paths.extend(new_paths)
        return paths

    def get_all_paths_between(self, start, end):
        if start not in self.adjacency or end not in self.adjacency:
            raise ValueError("Ошибка: обе вершины должны существовать")
        if start == end:
            return []
        return self.__dfs(start, end, [], {start})

    def get_shortest_distances_to(self, target):
        if target not in self.adjacency:
            raise ValueError(f"Ошибка: вершина '{target}' не существует")

        adjacency_reverse = {v: {} for v in self.adjacency}
        for u in self.adjacency:
            for v, w in self.adjacency[u].items():
                adjacency_reverse[v][u] = w

        distances = {}
        queue = deque([target])
        distances[target] = 0
        while queue:
            curr = queue.popleft()
            for neighbor in adjacency_reverse[curr]:
                if neighbor not in distances:
                    distances[neighbor] = distances[curr] + 1
                    queue.append(neighbor)
        return distances

    def __find_parent(self, v, parent):
        if parent[v] != v:
            parent[v] = self.__find_parent(parent[v], parent)
        return parent[v]

    def get_kruskal_mst(self):
        if self.directed or not self.weighted:
            raise ValueError("Ошибка: для алгоритм Краскала требуется неориентированный взвешенный граф")

        edges = self.get_edges()
        edges.sort(key=lambda e: e[2])

        parent = {}
        rank = {}
        for v in self.adjacency:
            parent[v] = v
            rank[v] = 0

        mst = Graph(directed=False, weighted=True)
        for v in self.adjacency:
            mst.add_vertex(v)

        for u, v, w in edges:
            if self.__find_parent(u, parent) != self.__find_parent(v, parent):
                ru = self.__find_parent(u, parent)
                rv = self.__find_parent(v, parent)
                if ru == rv:
                    continue
                if rank[ru] < rank[rv]:
                    parent[ru] = rv
                elif rank[ru] > rank[rv]:
                    parent[rv] = ru
                else:
                    parent[rv] = ru
                    rank[ru] += 1
                mst.add_edge(u, v, w)

        return mst

    # def get_shortest_path_bellman_ford(self, start, end):
    #     if start not in self.adjacency or end not in self.adjacency:
    #         raise ValueError("Ошибка: обе вершины должны существовать")
    #
    #     inf = float("inf")
    #     d = {v: inf for v in self.adjacency}
    #     parent = {v: None for v in self.adjacency}
    #     d[start] = 0
    #
    #     edges = []
    #     for u in self.adjacency:
    #         for v, w in self.adjacency[u].items():
    #             edges.append((u, v, w))
    #
    #     for _ in range(len(self.adjacency) - 1):
    #         is_updated = False
    #         for u, v, w in edges:
    #             if d[u] != inf and d[v] > d[u] + w:
    #                 d[v] = d[u] + w
    #                 parent[v] = u
    #                 is_updated = True
    #         if not is_updated:
    #             break
    #
    #     for u, v, w in edges:
    #         if d[u] != inf and d[v] > d[u] + w:
    #             raise ValueError("Ошибка: граф содержит отрицательный цикл")
    #
    #     if d[end] == inf:
    #         return inf, []
    #     return d[end], parent
    #
    # @staticmethod
    # def restore_path_from_parent(parent, end):
    #     path = []
    #     curr = end
    #     while curr is not None:
    #         path.append(curr)
    #         curr = parent[curr]
    #     path.reverse()
    #     return path
    #
    # def get_shortest_paths_dijkstra(self, start):
    #     if start not in self.adjacency:
    #         raise ValueError(f"Ошибка: вершина '{start}' не существует")
    #     if self.weighted and any(w < 0 for neighbors in self.adjacency.values() for w in neighbors.values()):
    #         raise ValueError("Ошибка: алгоритм Дейкстры не работает с отрицательными весами")
    #
    #     inf = float("inf")
    #     d = {v: inf for v in self.adjacency}
    #     parent = {v: None for v in self.adjacency}
    #     d[start] = 0
    #     q = [(0, start)]
    #
    #     while q:
    #         curr_dist, u = heapq.heappop(q)
    #         if curr_dist > d[u]:
    #             continue
    #         for v, w in self.adjacency[u].items():
    #             new_dist = curr_dist + w
    #             if d[v] > new_dist:
    #                 d[v] = new_dist
    #                 parent[v] = u
    #                 heapq.heappush(q, (new_dist, v))
    #     return d, parent
    #
    # def get_all_shortest_paths_floyd(self):
    #     vertexes = list(self.adjacency.keys())
    #     d = {u: {v: float("inf") for v in vertexes} for u in vertexes}
    #     next = {u: {v: None for v in vertexes} for u in vertexes}
    #
    #     for u in vertexes:
    #         d[u][u] = 0
    #         for v, w in self.adjacency[u].items():
    #             d[u][v] = w
    #             next[u][v] = v
    #
    #     for k in vertexes:
    #         for i in vertexes:
    #             for j in vertexes:
    #                 if d[i][j] > d[i][k] + d[k][j]:
    #                     d[i][j] = d[i][k] + d[k][j]
    #                     next[i][j] = next[i][k]
    #
    #     for u in vertexes:
    #         if d[u][u] < 0:
    #             raise ValueError("Ошибка: граф содержит отрицательный цикл")
    #
    #     return d, next
    #
    # @staticmethod
    # def restore_path_floyd(next, u, v):
    #     path = [u]
    #     while u != v:
    #         u = next[u][v]
    #         path.append(u)
    #     return path

    def get_shortest_path_floyd(self, start, end):
        if start not in self.adjacency or end not in self.adjacency:
            raise ValueError("Ошибка: обе вершины должны существовать")

        inf = float("inf")
        vertexes = list(self.adjacency.keys())
        d = {u: {v: inf for v in vertexes} for u in vertexes}
        next = {u: {v: None for v in vertexes} for u in vertexes}

        for u in vertexes:
            d[u][u] = 0
            for v, w in self.adjacency[u].items():
                d[u][v] = w
                next[u][v] = v

        for k in vertexes:
            for i in vertexes:
                for j in vertexes:
                    if d[i][j] > d[i][k] + d[k][j]:
                        d[i][j] = d[i][k] + d[k][j]
                        next[i][j] = next[i][k]

        for v in vertexes:
            if d[v][v] < 0:
                raise ValueError("Ошибка: граф содержит отрицательный цикл")

        if d[start][end] == inf:
            return inf, []

        return d[start][end], next

    @staticmethod
    def restore_path_floyd(next, u, v):
        path = [u]
        while u != v:
            u = next[u][v]
            path.append(u)
        return path

    def get_shortest_paths_bellman_ford(self, start):
        if not self.directed:
            raise ValueError(f"Ошибка: текущий граф неориентированный")

        if start not in self.adjacency:
            raise ValueError(f"Ошибка: вершина '{start}' не существует")

        inf = float("inf")
        d = {v: inf for v in self.adjacency}
        parent = {v: None for v in self.adjacency}
        d[start] = 0

        edges = []
        for u in self.adjacency:
            for v, w in self.adjacency[u].items():
                edges.append((u, v, w))

        for _ in range(len(self.adjacency) - 1):
            is_updated = False
            for u, v, w in edges:
                if d[u] != inf and d[v] > d[u] + w:
                    d[v] = d[u] + w
                    parent[v] = u
                    is_updated = True
            if not is_updated:
                break

        for u, v, w in edges:
            if d[u] != inf and d[v] > d[u] + w:
                raise ValueError("Ошибка: граф содержит отрицательный цикл")

        return d, parent

    @staticmethod
    def restore_path_from_parent(parent, end):
        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = parent[curr]
        path.reverse()
        return path

    def get_all_shortest_paths_dijkstra(self):
        if self.weighted and any(w < 0 for neighbors in self.adjacency.values() for w in neighbors.values()):
            raise ValueError("Ошибка: алгоритм Дейкстры не работает с отрицательными весами")

        vertexes = list(self.adjacency.keys())
        all_dist = {v: {} for v in vertexes}
        all_parent = {v: {} for v in vertexes}

        for start in vertexes:
            dist, parent = self.__get_shortest_paths_dijkstra(start)
            for v in vertexes:
                all_dist[start][v] = dist[v]
                all_parent[start][v] = parent[v]
        return all_dist, all_parent

    def __get_shortest_paths_dijkstra(self, start):
        d = {v: float("inf") for v in self.adjacency}
        parent = {v: None for v in self.adjacency}
        d[start] = 0
        q = [(0, start)]

        while q:
            curr_dist, u = heapq.heappop(q)
            if curr_dist > d[u]:
                continue
            for v, w in self.adjacency[u].items():
                new_dist = curr_dist + w
                if d[v] > new_dist:
                    d[v] = new_dist
                    parent[v] = u
                    heapq.heappush(q, (new_dist, v))
        return d, parent

    def get_max_flow(self, source, sink):
        if not self.directed:
            raise ValueError(f"Ошибка: текущий граф неориентированный")
        if source not in self.adjacency or sink not in self.adjacency:
            raise ValueError("Ошибка: источник или сток не существуют")
        if source == sink:
            raise ValueError("Ошибка: источник и сток должны отличаться")

        residual = defaultdict(lambda: defaultdict(int))
        for u in self.adjacency:
            for v, w in self.adjacency[u].items():
                residual[u][v] = w

        total_flow = 0
        inf = float("inf")

        while True:
            parent = {}
            parent[source] = source
            q = deque([source])
            while q and sink not in parent:
                u = q.popleft()
                for v, capacity in residual[u].items():
                    if capacity > 0 and v not in parent:
                        parent[v] = u
                        q.append(v)

            if sink not in parent:
                break

            bottleneck = inf
            v = sink
            while v != source:
                u = parent[v]
                bottleneck = min(bottleneck, residual[u][v])
                v = u

            v = sink
            while v != source:
                u = parent[v]
                residual[u][v] -= bottleneck
                residual[v][u] += bottleneck
                v = u

            total_flow += bottleneck

        return total_flow

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file_out:
            file_out.write(f"{int(self.directed)} {int(self.weighted)}\n")
            vertexes = sorted(self.adjacency.keys())
            file_out.write(" ".join(vertexes) + "\n")
            edges = set()
            for u in vertexes:
                for v, w in self.adjacency[u].items():
                    if self.directed:
                        if self.weighted:
                            file_out.write(f"{u} {v} {w}\n")
                        else:
                            file_out.write(f"{u} {v}\n")
                    else:
                        if (u, v) not in edges and (v, u) not in edges:
                            edges.add((u, v))
                            if self.weighted:
                                file_out.write(f"{u} {v} {w}\n")
                            else:
                                file_out.write(f"{u} {v}\n")

    def __str__(self):
        lines = []
        for v in sorted(self.adjacency.keys()):
            neighbors = self.adjacency[v]
            if neighbors:
                if self.weighted:
                    neighbors_str = ", ".join(f"{n} ({w})" for n, w in neighbors.items())
                else:
                    neighbors_str = ", ".join(neighbors.keys())
                lines.append(f"{v} -> {neighbors_str}")
            else:
                lines.append(f"{v} -> ...")
        return "\n".join(lines)
