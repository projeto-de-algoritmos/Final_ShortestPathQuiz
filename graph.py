INF = 999999


class Graph:

    def floyd_warshall(self, graph, n_vertices):
        distance = list(map(lambda i: list(map(lambda j: j, i)), graph))
        for k in range(n_vertices):
            for i in range(n_vertices):
                for j in range(n_vertices):
                    distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
        return distance

    def print_solution(self, distance, n_vertices):
        for i in range(n_vertices):
            for j in range(n_vertices):
                if distance[i][j] == INF:
                    print("INF", end=" ")
                else:
                    print(distance[i][j], end="  ")
            print(" ")
