from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from DAO.update import Update

class UpdateGoods(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.db = Update()
        self.cursor = self.db.connectdb()

        self.show()

    def initUI(self):
        self.setGeometry(50,50,550,350)
        self.setWindowTitle("更新商品")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # 商品编号
        self.numberInput = QLineEdit(self)
        self.numberInput.setGeometry(47.5, 40, 180, 35)
        self.numberInput.setPlaceholderText("商品编号")
        self.numberInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 名称
        self.nameInput = QLineEdit(self)
        self.nameInput.setGeometry(322.5, 40, 180, 35)
        self.nameInput.setPlaceholderText("名称")
        self.nameInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 数量
        self.amountInput = QLineEdit(self)
        self.amountInput.setGeometry(47.5, 115, 180, 35)
        self.amountInput.setPlaceholderText("数量")
        self.amountInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 单位
        self.unitInput = QLineEdit(self)
        self.unitInput.setGeometry(322.5, 115, 180, 35)
        self.unitInput.setPlaceholderText("单位")
        self.unitInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 价格
        self.priceInput = QLineEdit(self)
        self.priceInput.setGeometry(47.5, 190, 180, 35)
        self.priceInput.setPlaceholderText("价格")
        self.priceInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 备注
        self.remarkInput = QLineEdit(self)
        self.remarkInput.setGeometry(322.5, 190, 180, 35)
        self.remarkInput.setPlaceholderText("备注")
        self.remarkInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        self.okBtn = QPushButton("确定",self)
        self.okBtn.setGeometry(137.5,265,275,40)
        self.okBtn.setStyleSheet("border-radius: 8px; background-color: #66ccff;border-color: red;border-style: solid")
        self.okBtn.clicked.connect(self.updateGoods)

    def updateGoods(self):
        number = self.numberInput.text()
        if number == "":
            QMessageBox.warning(self,"警告","商品编号不能为空！",QMessageBox.Yes)
            return
        else:
            price = self.priceInput.text()
            index = price.find(".")
            if index >= 0:
                substr = price[index+1:]
                if len(substr) > 2:
                    QMessageBox.warning(self, "警告", "价格超过两位小数！", QMessageBox.Yes)
                    return

            name = self.nameInput.text()
            amount = self.amountInput.text()
            unit = self.unitInput.text()
            price = self.priceInput.text()
            remark = self.remarkInput.text()

            sql = "update goods set name = %s , amount = %s , unit = %s , price = %s , remark = %s where number = %s"
            res = self.db.update(self.cursor,sql,(name,int(amount),unit,float(price),remark,number))
            if res == 1:
                QMessageBox.information(self,"提示","修改成功！",QMessageBox.Yes)
            else:
                QMessageBox.information(self, "提示", "修改失败！", QMessageBox.Yes)

    def closeEvent(self, QCloseEvent):
        self.db.db.close()
        print("更新商品窗口关闭")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = UpdateGoods()
    sys.exit(app.exec_())