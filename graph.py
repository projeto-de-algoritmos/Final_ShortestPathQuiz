from networkx.generators.stochastic import stochastic_graph
from networkx.generators.random_graphs import erdos_renyi_graph
import random
import numpy as np

INF = 999999

class Graph:
    colors = [
            '#000000',
            '#FF0000',
            '#FFFF00',
            '#00FF00',
            '#008000',
            '#00FFFF',
            '#0000FF',
            '#FF00FF',
            '#808080'
        ]
    tableResult = None

    def __init__(self, qtdNodes):
        self.graph = erdos_renyi_graph(qtdNodes, 0.5, directed=True)
        self.nodes = qtdNodes
        self.graphTable = np.zeros((self.nodes, self.nodes)).astype(int)

        stochastic_graph(self.graph)

        self.initializeGraphTable()
        self.randomizeWeight()

    def getColors(self):
        return self.colors

    def getGraph(self):
        return self.graph

    def initializeGraphTable(self):
        for i in range(self.nodes):
            for j in range(self.nodes):
                if i != j:
                    self.graphTable[i][j] = INF

    def floydWarshall(self):
        self.tableResult = self.graphTable
        for k in range(self.nodes):
            for i in range(self.nodes):
                for j in range(self.nodes):
                    self.tableResult[i][j] = min(self.tableResult[i][j], self.tableResult[i][k] + self.tableResult[k][j])

    def printSolution(self):
        for i in range(self.nodes):
            for j in range(self.nodes):
                if self.tableResult[i][j] == INF:
                    print("-", end="\t")
                else:
                    print(self.tableResult[i][j], end="\t")
            print(" ")

    def randomizeWeight(self):
        for (u, v, w) in self.graph.edges(data=True):

            existingEdge = [e for e in self.graph.out_edges(v) if e == (v, u)]
            
            if(len(existingEdge) == 0 or self.graphTable[v][u] == INF):
                w['weight'] = random.randint(1, 20)
            else:
                w['weight'] = self.graphTable[v][u]

            self.graphTable[u][v] = w['weight']
            w['color'] = random.choice(self.colors)
        #     print(u, v, w['weight'])
        # print()

