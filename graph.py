from collections import deque


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
