from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import hashlib
import uuid


from DAO.insert import Insert


class InsertPersons(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Insert()
        self.cursor = self.db.connectdb()

        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(100,100,300,350)
        self.setWindowTitle("添加会员")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText("会员姓名")
        self.nameInput.setGeometry(50,50,200,40)
        self.nameInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setPlaceholderText("密码")
        self.passwordInput.setGeometry(50,120,200,40)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        self.telephoneInput = QLineEdit(self)
        self.telephoneInput.setPlaceholderText("联系电话")
        self.telephoneInput.setGeometry(50,190,200,40)
        self.telephoneInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        self.okBtn = QPushButton("确定",self)
        self.okBtn.setGeometry(50,260,200,40)
        self.okBtn.setStyleSheet("border-radius: 8px; background-color: #66ccff;border-color: red;border-style: solid")
        self.okBtn.clicked.connect(self.insertPersons)

    def genNumber(self):
        number = str(uuid.uuid1())
        number = number.split('-')
        number = ''.join(number)
        return number[8:16]

    def insertPersons(self):
        name = self.nameInput.text()
        if name == '':
            QMessageBox.warning(self,"警告","会员名称不能为空！",QMessageBox.Yes)
            return

        password = self.passwordInput.text()
        if password == '':
            QMessageBox.warning(self,"警告","密码不能为空！",QMessageBox.Yes)
            return

        telephone = self.telephoneInput.text()
        if telephone == '':
            QMessageBox.warning(self,"警告","联系电话不能为空！",QMessageBox.Yes)
            return

        m = hashlib.md5()
        m.update(password.encode("utf-8"))
        password = m.hexdigest()


        number = self.genNumber()
        sql = "insert into persons(number,name,password,telephone) VALUES(%s,%s,%s,%s)"
        values = (number,name,password,telephone)
        print(values)
        res = self.db.insert(self.cursor,sql,values)
        if res == 1:
            QMessageBox.information(self, "提示", "添加成功！", QMessageBox.Yes)
        else:
            QMessageBox.information(self, "提示", "添加失败，请重新检查信息！", QMessageBox.Yes)

    def closeEvent(self, QCloseEvent):
        self.db.db.close()
        print("添加会员窗口关闭")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = InsertPersons()
    sys.exit(app.exec_())