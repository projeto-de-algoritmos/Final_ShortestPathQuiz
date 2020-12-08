from networkx.generators.stochastic import stochastic_graph
from networkx.generators.random_graphs import erdos_renyi_graph
import random
import numpy as np
import copy

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

    def __init__(self, qtdNodes):
        self.graph = erdos_renyi_graph(qtdNodes, 0.5, directed=True)
        self.nodes = qtdNodes
        self.graphTable = np.zeros((self.nodes, self.nodes)).astype(int)
        self.colorTable = np.zeros((self.nodes, self.nodes)).astype(str)

        stochastic_graph(self.graph)

        self.initializeGraphTable()
        self.randomizeWeight()

    def getColors(self):
        return self.colors

    def getGraph(self):
        return self.graph

    def getCorrectTable(self):
        correctTable = copy.deepcopy(self.resultTable)
        for i in range(self.nodes):
            for j in range(self.nodes):
                if self.resultTable[i][j] == str(INF):
                    correctTable[i][j] = '-'
        return correctTable

    def getAnswerTable(self):
        return self.answerTable
    
    def putIncognitos(self):
        self.answerTable = copy.deepcopy(self.resultTable)
        for i in range(self.nodes):
            for j in range(self.nodes):
                if (random.random() < 0.5 and self.answerTable[i][j] != str(INF) and self.answerTable[i][j] != '0'):
                    self.answerTable[i][j] = ''
                if self.resultTable[i][j] == str(INF):
                    self.answerTable[i][j] = '-'

    def initializeGraphTable(self):
        for i in range(self.nodes):
            for j in range(self.nodes):
                if i != j:
                    self.graphTable[i][j] = INF

    def floydWarshall(self):
        self.resultTable = self.graphTable

        for k in range(self.nodes):
            for i in range(self.nodes):
                for j in range(self.nodes):
                    self.resultTable[i][j] = min(self.resultTable[i][j], self.resultTable[i][k] + self.resultTable[k][j])
        self.resultTable = self.resultTable.astype('U')
        self.putIncognitos()
    
    def printSolution(self):
        for i in range(self.nodes):
            for j in range(self.nodes):
                if self.resultTable[i][j] == str(INF):
                    print("-", end="\t")
                else:
                    print(self.resultTable[i][j], end="\t")
            print(" ")

    def randomizeWeight(self):
        for (u, v, w) in self.graph.edges(data=True):

            existingEdge = [e for e in self.graph.out_edges(v) if e == (v, u)]
            
            if(len(existingEdge) == 0 or self.graphTable[v][u] == INF):
                w['weight'] = random.randint(1, 20)
                w['color'] = random.choice(self.colors)
            else:
                w['weight'] = self.graphTable[v][u]
                w['color'] = self.colorTable[v][u]

            self.graphTable[u][v] = w['weight']
            self.colorTable[u][v] = w['color']
        #     print(u, v, w)
        # print()

