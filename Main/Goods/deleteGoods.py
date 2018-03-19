from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from DAO.delete import Delete
from DAO.select import Select


class DeleteGoods(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.db = Delete()
        self.cursor = self.db.connectdb()

        self.show()

    def initUI(self):
        self.setGeometry(50,50,300,200)
        self.setWindowTitle("添加商品")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # 商品编号
        self.numberInput = QLineEdit(self)
        self.numberInput.setGeometry(50, 30, 200, 40)
        self.numberInput.setPlaceholderText("商品编号")
        self.numberInput.setStyleSheet("border-radius: 8px; background-color: #FFF5EE;border-color: red;border-style: solid")

        self.deleteBtn = QPushButton("删除",self)
        self.deleteBtn.setGeometry(75,100,150,40)
        self.deleteBtn.setStyleSheet("border-radius: 8px; background-color: #cc0000;border-color: red;border-style: solid")
        self.deleteBtn.clicked.connect(self.deleteGoods)

    def deleteGoods(self):
        number = self.numberInput.text()
        if number == "":
            QMessageBox.warning(self,"警告","商品编号不能为空！",QMessageBox.Yes)
            return
        else:
            if self.judgeExists(number) == -1:
                QMessageBox.warning(self,"错误","该商品不存在",QMessageBox.Yes);
                self.numberInput.setText("")
                return
            else:
                sql = "delete from goods where number = %s"
                print(number)
                values = (number)
                res = self.db.delete(self.cursor, sql, values)
                if res == 1:
                    QMessageBox.information(self, "提示", "删除成功！", QMessageBox.Yes)
                else:
                    QMessageBox.warning(self, "提示", "该商品不存在！", QMessageBox.Yes)

    def judgeExists(self,number):
        select = Select()
        cursor = select.connectdb()

        sql = "select * from goods where number = %s"
        values = (number)
        counts,results = select.select(cursor,sql,values)
        if counts == 0:
            select.db.close()
            return -1
        else:
            select.db.close()
            return 1

    def closeEvent(self, QCloseEvent):
        self.db.db.close()
        print("删除商品窗口关闭")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = DeleteGoods()
    sys.exit(app.exec_())