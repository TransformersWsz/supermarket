from PyQt5.QtWidgets import *
import sys

from MyOwn.b import B

class A(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle("A窗口")
        self.setGeometry(10,100,300,300)

        self.inputLine = QLineEdit(self)
        self.inputLine.setText("A窗口")
        self.inputLine.setGeometry(10,10,50,30)


        self.aBtn = QPushButton("new B",self)
        self.aBtn.setGeometry(10,80,100,30)
        self.aBtn.clicked.connect(self.createBWin)

        self.changeValueBtn = QPushButton("changevalue", self)
        self.changeValueBtn.setGeometry(10, 200, 100, 30)
        self.changeValueBtn.clicked.connect(lambda: self.bWin.changeValue(self.inputLine.text()))
        self.changeValueBtn.clicked.connect(lambda: self.bWin.cWin.changeValue(self.inputLine.text()))

        self.inputLine.textChanged[str].connect(lambda: self.bWin.changeValue(self.inputLine.text()))
        self.inputLine.textChanged[str].connect(lambda: self.bWin.cWin.changeValue(self.inputLine.text()))

    def createBWin(self):
        self.bWin = B(self)


    def changeValue(self,newValue):
        self.inputLine.setText(newValue)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = A()
    sys.exit(app.exec_())