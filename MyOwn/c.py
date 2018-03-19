from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys


class C(QWidget):
    def __init__(self, BWin):
        super().__init__()
        self.initUI()
        self.show()
        self.bWin = BWin

    def initUI(self):
        self.setWindowTitle("C窗口")
        self.setGeometry(900, 100, 300, 300)

        self.inputLine = QLineEdit(self)
        self.inputLine.setGeometry(10, 10, 100, 20)

        self.changeValueBtn = QPushButton("changevalue", self)
        self.changeValueBtn.setGeometry(10, 200, 100, 30)
        self.changeValueBtn.clicked.connect(lambda: self.bWin.changeValue(self.inputLine.text()))
        self.changeValueBtn.clicked.connect(lambda: self.bWin.aWin.changeValue(self.inputLine.text()))

    def changeValue(self,newValue):
        self.inputLine.setText(newValue)