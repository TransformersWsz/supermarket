from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from DAO.insert import Insert


class InsertGoods(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Insert()
        self.cursor = self.db.connectdb()

        self.initUI()



        self.show()

    def closeEvent(self, QCloseEvent):
        self.db.db.close()
        print("添加商品窗口关闭")

    def initUI(self):
        self.setGeometry(50,50,400,500)
        self.setWindowTitle("添加商品")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # 商品编号
        self.numberInput = QLineEdit(self)
        self.numberInput.setGeometry(100, 10, 200, 40)
        self.numberInput.setPlaceholderText("商品编号")
        self.numberInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 名称
        self.nameInput = QLineEdit(self)
        self.nameInput.setGeometry(30, 60, 140, 40)
        self.nameInput.setPlaceholderText("名称")
        self.nameInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 备注
        self.remarkInput = QLineEdit(self)
        self.remarkInput.setGeometry(230, 60, 140, 40)
        self.remarkInput.setPlaceholderText("备注")
        self.remarkInput.setStyleSheet(
            "border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 数量
        self.amountInput = QLineEdit(self)
        self.amountInput.setGeometry(30, 140, 140, 40)
        self.amountInput.setPlaceholderText("数量")
        self.amountInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 单位
        self.unitInput = QLineEdit(self)
        self.unitInput.setGeometry(230, 140, 140, 40)
        self.unitInput.setPlaceholderText("单位")
        self.unitInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 价格
        self.priceInput = QLineEdit(self)
        self.priceInput.setGeometry(30, 220, 140, 40)
        self.priceInput.setPlaceholderText("价格")
        self.priceInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 保质期
        self.lifeInput = QLineEdit(self)
        self.lifeInput.setGeometry(230, 220, 140, 40)
        self.lifeInput.setPlaceholderText("保质期")
        self.lifeInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 联系电话
        self.telephoneInput = QLineEdit(self)
        self.telephoneInput.setGeometry(30, 300, 140, 40)
        self.telephoneInput.setPlaceholderText("联系电话")
        self.telephoneInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 生产地址
        self.produceaddressInput = QLineEdit(self)
        self.produceaddressInput.setGeometry(230, 300, 140, 40)
        self.produceaddressInput.setPlaceholderText("生产地址")
        self.produceaddressInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 生产日期
        self.producedateInput = QLineEdit(self)
        self.producedateInput.setGeometry(30, 380, 140, 40)
        self.producedateInput.setPlaceholderText("生产日期")
        self.producedateInput.setStyleSheet(
            "border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")

        # 生产厂商
        self.producerInput = QLineEdit(self)
        self.producerInput.setGeometry(230, 380, 140, 40)
        self.producerInput.setPlaceholderText("生产厂商")
        self.producerInput.setStyleSheet("border-radius: 8px; background-color: #EEE5DE;border-color: red;border-style: solid")


        self.okBtn = QPushButton("确定",self)
        self.okBtn.setGeometry(100,440,200,40)
        self.okBtn.setStyleSheet("border-radius: 8px; background-color: #66ccff;border-color: red;border-style: solid")
        self.okBtn.clicked.connect(self.insertGoods)

    def insertGoods(self):
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

            if self.amountInput.text() == '':
                amount = 0
            else:
                amount = int(self.amountInput.text())

            unit = self.unitInput.text()

            if self.priceInput.text() == '':
                price = 0
            else:
                price = float(self.priceInput.text())

            if self.lifeInput.text() == '':
                life = 0
            else:
                life = int(self.lifeInput.text())

            telephone = self.telephoneInput.text()
            produceaddress = self.produceaddressInput.text()
            producedate = self.producedateInput.text()
            producer = self.producerInput.text()
            remark = self.remarkInput.text()

            sql = "insert into goods(number,name,amount,unit,price,life,telephone,produceaddress,producedate,producer,remark) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = (number,name,amount,unit,price,life,telephone,produceaddress,producedate,producer,remark)
            print(values)
            res = self.db.insert(self.cursor,sql,values)
            if res == 1:
                QMessageBox.information(self,"提示","添加成功！",QMessageBox.Yes)
            else:
                QMessageBox.information(self, "提示", "添加失败，请重新检查信息！", QMessageBox.Yes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = InsertGoods()
    sys.exit(app.exec_())