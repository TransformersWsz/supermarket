from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import hashlib
import logging

from DAO.select import Select
from Main.mainWindow import MainWindow





class Login(QMainWindow):
    def __init__(self):
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

        super().__init__()
        self.setWindowTitle("登陆")

        # 设置背景图片
        palette = QPalette()

        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("login.jpg")))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.setGeometry(200, 300, 600, 390)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.account = QLineEdit(self)
        self.account.setGeometry(175,100,250,35)
        self.account.setPlaceholderText("帐号")
        self.account.setStyleSheet("border-radius: 12px; background-color: #F8F8FF;border-color: red;border-style: solid")

        self.password = QLineEdit(self)
        self.password.setGeometry(175, 170, 250, 35)
        self.password.setPlaceholderText("密码")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("border-radius: 12px; background-color: #F8F8FF;border-color: red;border-style: solid")

        btn = QPushButton("登陆",self)
        btn.setGeometry(175,240,250,35)
        btn.setStyleSheet("border-color: 2px;border-style: solid;border-color: red;background-color: #63B8FF;border-radius: 10px;color:#ffffff")
        btn.clicked.connect(self.enterMainWindow)
        self.show()

    # def log(self):
    #     def decorator(func):
    #         def wrapper():
    #             account = func()
    #             info = "%s登陆成功" % (account)
    #             logging.debug(info)
    #         return wrapper
    #     return decorator


    #
    # def enterMainWindow1(self):
    #     self.enterMainWindow()


    def enterMainWindow(self):
        account = self.account.text()
        if account == "":
            QMessageBox.warning(self,"警告","帐号不能为空！",QMessageBox.Yes)
            return -1

        password = self.password.text()
        if password == "":
            QMessageBox.warning(self,"警告","密码不能为空！",QMessageBox.Yes)
            return -2

        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        password = m.hexdigest()

        select = Select()
        cursor = select.connectdb()
        sql = "select * from `employee` where account = %s and password = %s"
        values = (account,password)
        counts,results = select.select(cursor,sql,values)
        if counts == 0:
            QMessageBox.warning(self,"错误","帐号或密码错误！",QMessageBox.Yes)
            return -3
        else:
            self.close()
            self.mainWindow = MainWindow()
            self.mainWindow.show()
            return account




if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()
    sys.exit(app.exec_())
