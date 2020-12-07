from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from networkx.generators.stochastic import stochastic_graph
from networkx.generators.random_graphs import erdos_renyi_graph
import networkx as nx
import random

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
        self.qtdNodesSpinBox.setMinimum(5)
        self.qtdNodesSpinBox.setMaximum(15)
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
        
        graph = erdos_renyi_graph(self.qtdNodesSpinBox.value(), 0.5,directed=True)

        stochastic_graph(graph)

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

        for (u, v, w) in graph.edges(data=True):
            w['weight'] = random.randint(1, 30)
            w['color'] = random.choice(colors)
            # print(u, v, w)
        
        pos = dict()

        pos.update( (n, (random.random()*10, random.random()*10)) for i, n in enumerate(set(graph.nodes(data=False))) ) # put nodes from X at x=1
        
        edgeColors = nx.get_edge_attributes(graph,'color')
        nx.draw(graph, pos=pos, width=1, with_labels=True, edge_color=colors)

        weights = nx.get_edge_attributes(graph,'weight')
        nx.draw_networkx_edge_labels(graph,pos, edge_labels=weights)

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
