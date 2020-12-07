from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from graph import Graph
import networkx as nx
import random

INF = 999999

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()        
        font = QFont()
        font.setPointSize(16)

        self.font14 = QFont()
        self.font14.setPointSize(14)

        self.font12 = QFont()
        self.font12.setPointSize(12)

        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 1280, 800)
        self.center()
        self.setWindowTitle('Game')

        grid = QGridLayout()
        self.setLayout(grid)
        self.createVerticalGroupBox() 

        buttonLayout = QVBoxLayout()
        buttonsWidget = self.verticalGroupBox
        buttonsWidget.setFixedWidth(200)
        buttonLayout.addWidget(buttonsWidget)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)        
        grid.addWidget(self.canvas, 0, 0, 9, 9)          
        grid.addLayout(buttonLayout, 0, 9)

        self.show()


    def createVerticalGroupBox(self):
        self.verticalGroupBox = QGroupBox()

        layout = QVBoxLayout()

        label = QLabel('Quantidade de nós')
        label.setFont(self.font14)
        layout.addWidget(label)

        self.qtdNodesSpinBox = QSpinBox()
        self.qtdNodesSpinBox.setFont(self.font12)
        self.qtdNodesSpinBox.setMinimum(4)
        self.qtdNodesSpinBox.setMaximum(10)
        self.qtdNodesSpinBox.setObjectName("qtdNodesSpinBox")
        layout.addWidget(self.qtdNodesSpinBox)

        generateGraphButton = QPushButton('Gerar grafo')
        generateGraphButton.setObjectName('generateGraphButton')
        generateGraphButton.setFont(self.font12)
        generateGraphButton.clicked.connect(self.generateGraphButton)
        layout.addWidget(generateGraphButton)
        layout.addSpacing(40)


        label = QLabel('Resposta')
        label.setFont(self.font14)
        layout.addWidget(label)

        self.answer = QLineEdit()
        self.answer.setObjectName('answer')
        self.answer.setFont(self.font12)
        layout.addWidget(self.answer)
        layout.addSpacing(10)

        replyButton = QPushButton('Responder')
        replyButton.setObjectName('replyButton')
        replyButton.setFont(self.font12)
        # replyButton.clicked.connect(self.reply)
        layout.addWidget(replyButton)
        layout.addSpacing(30)
        
        self.verticalGroupBox.setLayout(layout)

    # def submitCommand(self):
    #     eval('self.' + str(self.sender().objectName()) + '()')

    def generateGraphButton(self):
        self.figure.clf()

        graph = Graph(self.qtdNodesSpinBox.value())

        graph.floydWarshall()
        graph.printSolution()
        print()

        pos = dict()

        pos.update((n, (random.random()*10, random.random()*10)) for i, n in enumerate(set(graph.getGraph().nodes(data=False)))) # put nodes from X at x=1
        
        edgeColors = nx.get_edge_attributes(graph.getGraph(), 'color')
        nx.draw(graph.getGraph(), pos=pos, width=1, with_labels=True, edge_color=graph.getColors())

        weights = nx.get_edge_attributes(graph.getGraph(), 'weight')
        nx.draw_networkx_edge_labels(graph.getGraph(), pos, edge_labels=weights)

        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def floyd_warshall(self, graph, n_vertices):
        distance = graph
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


if __name__ == '__main__':

    import sys  
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = MainWindow() 
    screen.show()   
    sys.exit(app.exec_())
