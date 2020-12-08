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
        buttonsWidget.setFixedWidth(250)
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
        generateGraphButton.clicked.connect(self.generateGraph)
        layout.addWidget(generateGraphButton)
        layout.addSpacing(60)


        label = QLabel('Resposta')
        label.setFont(self.font14)
        layout.addWidget(label)

        self.answerTable = QTableWidget()
        self.answerTable.setObjectName('answerTable')
        self.answerTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        font = QFont()
        font.setPointSize(10)

        self.answerTable.setFont(font)
        layout.addWidget(self.answerTable)
        layout.addSpacing(10)

        self.replyButton = QPushButton('Responder')
        self.replyButton.setObjectName('replyButton')
        self.replyButton.setFont(self.font12)
        self.replyButton.clicked.connect(self.reply)
        self.replyButton.setEnabled(False)
        layout.addWidget(self.replyButton)
        layout.addSpacing(30)
        
        self.verticalGroupBox.setLayout(layout)

    def generateTable(self, table):
        self.answerTable.setRowCount(len(table))
        self.answerTable.setColumnCount(len(table))
        self.answerTable.setVerticalHeaderLabels([str(i) for i in range(len(table))])
        self.answerTable.setHorizontalHeaderLabels([str(i) for i in range(len(table))])

        for i in range(len(table)):
            for j in range(len(table)):
                value = QTableWidgetItem(table[i][j])
                value.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                if(table[i][j] != ''):
                    value.setFlags(value.flags() ^ Qt.ItemIsEditable)

                self.answerTable.setItem(i, j, value)
                # print(self.answerTable.item(i,j).text())

    def reply(self):
        correctTable = self.graph.getCorrectTable()
        answerTable = self.graph.getAnswerTable()

        for i in range(len(correctTable)):
            for j in range(len(correctTable)):
                if(answerTable[i][j] == ''):
                    if(self.answerTable.item(i,j).text() == correctTable[i][j]):
                        self.answerTable.item(i,j).setBackground(Qt.green)
                    else:
                        self.answerTable.item(i,j).setBackground(Qt.red)


    def generateGraph(self):
        self.figure.clf()

        self.graph = Graph(self.qtdNodesSpinBox.value())

        self.graph.floydWarshall()

        # self.graph.printSolution()
        # print()

        self.generateTable(self.graph.getAnswerTable())

        pos = dict()

        pos.update((n, (random.random()*10, random.random()*10)) for i, n in enumerate(set(self.graph.getGraph().nodes(data=False)))) # put nodes from X at x=1
        
        edgeColors = nx.get_edge_attributes(self.graph.getGraph(), 'color')
        nx.draw(self.graph.getGraph(), pos=pos, width=1, with_labels=True, edge_color=edgeColors.values())

        weights = nx.get_edge_attributes(self.graph.getGraph(), 'weight')
        nx.draw_networkx_edge_labels(self.graph.getGraph(), pos, edge_labels=weights)

        self.replyButton.setEnabled(True)
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    import sys  
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = MainWindow() 
    screen.show()   
    sys.exit(app.exec_())
