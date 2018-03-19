from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from MyOwn.c import C

class B(QWidget):
    def __init__(self,AWin):
        super().__init__()
        self.initUI()
        self.show()
        self.aWin = AWin

    def initUI(self):
        self.setWindowTitle("B窗口")
        self.setGeometry(500, 100, 300, 300)

        self.inputLine = QLineEdit(self)
        self.inputLine.setGeometry(10,10,100,20)

        self.bBtn = QPushButton("new C",self)
        self.bBtn.setGeometry(10, 50, 100, 30)
        self.bBtn.clicked.connect(self.createCwin)

        self.changeValueBtn = QPushButton("changevalue", self)
        self.changeValueBtn.setGeometry(10, 200, 100, 30)
        self.changeValueBtn.clicked.connect(lambda: self.aWin.changeValue(self.inputLine.text()))
        self.changeValueBtn.clicked.connect(lambda: self.cWin.changeValue(self.inputLine.text()))

    def createCwin(self):
        self.cWin = C(self)

    def changeValue(self,newValue):
        self.inputLine.setText(newValue)