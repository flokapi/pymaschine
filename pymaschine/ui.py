



from PyQt5.QtWidgets import *




class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        layout = QVBoxLayout()
        layout.addWidget(QPushButton('Welcome To PyMaschine'))
        layout.addWidget(QPushButton('Bottom'))

        mainBox = QWidget()
        mainBox.setLayout(layout)
        self.setCentralWidget(mainBox)

        self.show()



def update():
    app.processEvents()



app = QApplication([])


mainWindow = MainWindow()
