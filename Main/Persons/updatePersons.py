from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import hashlib

from DAO.update import Update
from DAO.select import Select

class UpdatePersons(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.db = Update()
        self.cursor = self.db.connectdb()

        self.show()

    def initUI(self):
        self.setGeometry(100,100,450,300)
        self.setWindowTitle("更新会员信息")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.numberInput = QLineEdit(self)
        self.numberInput.setGeometry(22.5,50,180,45)
        self.numberInput.setPlaceholderText("会员账号")
        self.numberInput.setStyleSheet("border-radius: 8px; background-color: #F8F8FF;border-color: red;border-style: solid")

        self.telephoneInput = QLineEdit(self)
        self.telephoneInput.setGeometry(247.5,50,180,45)
        self.telephoneInput.setPlaceholderText("联系电话，默认保留原有号码")
        self.telephoneInput.setStyleSheet("border-radius: 8px; background-color: #F8F8FF;border-color: red;border-style: solid")

        self.oldpasswordInput = QLineEdit(self)
        self.oldpasswordInput.setGeometry(22.5,130,180,45)
        self.oldpasswordInput.setPlaceholderText("旧密码")
        self.oldpasswordInput.setEchoMode(QLineEdit.Password)
        self.oldpasswordInput.setStyleSheet("border-radius: 8px; background-color: #F8F8FF;border-color: red;border-style: solid")

        self.newpasswordInput = QLineEdit(self)
        self.newpasswordInput.setGeometry(247.5, 130, 180, 45)
        self.newpasswordInput.setPlaceholderText("新密码，默认保留原有密码")
        self.newpasswordInput.setEchoMode(QLineEdit.Password)
        self.newpasswordInput.setStyleSheet("border-radius: 8px; background-color: #F8F8FF;border-color: red;border-style: solid")

        self.okBtn = QPushButton("确定",self)
        self.okBtn.setGeometry(75,200,300,50)
        self.okBtn.setStyleSheet("border-radius: 8px; background-color: #66ccff;border-color: red;border-style: solid")
        self.okBtn.clicked.connect(self.updatePersons)


    def updatePersons(self):
        telephone = self.telephoneInput.text()
        number = self.numberInput.text()
        if number == "":
            QMessageBox.warning(self,"警告","会员账号不能为空！",QMessageBox.Yes)
            return

        oldpassword = self.oldpasswordInput.text()
        if oldpassword == "":
            QMessageBox.warning(self, "警告", "密码不能为空！", QMessageBox.Yes)
            return

        newpassword = self.newpasswordInput.text()
        if newpassword == "" and telephone == "":
            QMessageBox.warning(self, "提示", "您的信息并未做任何修改！", QMessageBox.Yes)
            return

        if newpassword == "" and telephone != "":
            isExists = self.judgeExists(number,oldpassword)
            if isExists == -1:
                QMessageBox.information(self, "提示", "帐号或密码错误！", QMessageBox.Yes)
                return
            else:
                m = hashlib.md5()
                m.update(oldpassword.encode('utf-8'))
                password = m.hexdigest()
                sql = "update persons set telephone = %s where number = %s and password = %s"
                values = (telephone,number,password)
                res = self.db.update(self.cursor,sql,values)
                if res == 1:
                    QMessageBox.information(self,"提示","修改成功！",QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", "帐号或密码错误！", QMessageBox.Yes)

        if newpassword != "" and telephone == "":
            isExists = self.judgeExists(number, oldpassword)
            if isExists == -1:
                QMessageBox.information(self, "提示", "帐号或密码错误！", QMessageBox.Yes)
                return
            else:
                m = hashlib.md5()
                m.update(oldpassword.encode('utf-8'))
                oldpassword = m.hexdigest()

                m.update(newpassword.encode('utf-8'))
                newpassword = m.hexdigest()

                sql = "update persons set password = %s where number = %s and password = %s"
                values = (newpassword,number,oldpassword)
                res = self.db.update(self.cursor, sql, values)
                if res == 1:
                    QMessageBox.information(self,"提示","修改成功！",QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", "帐号或密码错误！", QMessageBox.Yes)

        if newpassword != "" and telephone != "":
            isExists = self.judgeExists(number, oldpassword)
            if isExists == -1:
                QMessageBox.information(self, "提示", "帐号或密码错误！", QMessageBox.Yes)
                return
            else:
                m = hashlib.md5()
                m.update(oldpassword.encode('utf-8'))
                oldpassword = m.hexdigest()

                m.update(newpassword.encode('utf-8'))
                newpassword = m.hexdigest()

                sql = "update persons set password = %s , telephone = %s where number = %s and password = %s"
                values = (newpassword , telephone , number , oldpassword)
                res = self.db.update(self.cursor, sql, values)
                if res == 1:
                    QMessageBox.information(self, "提示", "修改成功！", QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "提示", "帐号或密码错误！", QMessageBox.Yes)


    def judgeExists(self,number,password):
        select = Select()
        cursor = select.connectdb()
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        password = m.hexdigest()

        sql = "select * from persons where number = %s and password = %s"
        values = (number,password)
        counts,results = select.select(cursor,sql,values)
        if counts == 0:
            select.db.close()
            return -1
        else:
            select.db.close()
            return 1

    def closeEvent(self, QCloseEvent):
        self.db.db.close()
        print("更新会员信息窗口关闭")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = UpdatePersons()
    sys.exit(app.exec_())