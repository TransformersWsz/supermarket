from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from DAO.select import Select
from Main.JieSuan.solveWidget import SolveWidget

class PaypalGoods(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Select()
        self.cursor = self.db.connectdb()

        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle("商品结算")
        self.setGeometry(100,100,500,350)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.rowcount = 0

        self.goodsNumberInput = QLineEdit(self)
        self.goodsNumberInput.setGeometry(45,17,180,35)
        self.goodsNumberInput.setPlaceholderText("请输入商品编号")
        self.goodsNumberInput.setStyleSheet("border-radius: 8px; background-color: #F8F8FF;border-color: red;border-style: solid")

        self.goodsAmountInput = QLineEdit(self)
        self.goodsAmountInput.setGeometry(270, 17, 180, 35)
        self.goodsAmountInput.setPlaceholderText("请输入商品数量")
        self.goodsAmountInput.setStyleSheet("border-radius: 8px; background-color: #F8F8FF;border-color: red;border-style: solid")

        self.addRowBtn = QPushButton("加入购物车",self)
        self.addRowBtn.setGeometry(175,68,150,30)
        self.addRowBtn.setStyleSheet("background-color:#63B8FF; border-width: 2px; border-radius: 3px")
        self.addRowBtn.clicked.connect(self.addRow)


        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(0,120,500,150)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["商品编号","名称","单价","数量"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        self.solveBtn = QPushButton("结算",self)
        self.solveBtn.setGeometry(175,300,150,30)
        self.solveBtn.setStyleSheet("background-color:#63B8FF; border-width: 2px; border-radius: 3px")
        self.solveBtn.clicked.connect(self.newSolveWidget)

    # 获得总消费金额
    def getTotalMoney(self):
        sum = 0
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        goods = []
        for row in range(rows):
            number = self.tableWidget.item(row,0).text()
            name = self.tableWidget.item(row,1).text()
            price = float(self.tableWidget.item(row,2).text())
            amount = float(self.tableWidget.item(row,3).text())
            good = (number,name,price,amount)
            goods.append(good)
            sum = sum + price * amount

        return sum,goods


    def addRow(self):
        number = self.goodsNumberInput.text()
        amount = self.goodsAmountInput.text()
        if number == "":
            QMessageBox.warning(self,"警告","商品编号不能为空！",QMessageBox.Yes)
        else:
            if amount == '':
                QMessageBox.warning(self, "警告", "商品数量不能为空！", QMessageBox.Yes)
            else:
                sql = "select number,name,price,amount from goods where number = %s"
                values = (number)
                counts,results = self.db.select(self.cursor,sql,values)

                print(results[0][3]," ",type(results[0][3]),"....")
                if results[0][3] < int(amount):
                    QMessageBox.warning(self, "警告", "该商品库存数量不足！请重新输入", QMessageBox.Yes)
                    self.goodsAmountInput.setText("")
                    return

                if counts != 0:
                    self.tableWidget.insertRow(self.rowcount)
                    for row in results:
                        item0 = QTableWidgetItem(str(row[0]))
                        item0.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                        self.tableWidget.setItem(self.rowcount, 0, item0)

                        item1 = QTableWidgetItem(str(row[1]))
                        item1.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                        self.tableWidget.setItem(self.rowcount, 1, item1)

                        item2 = QTableWidgetItem(str(row[2]))
                        item2.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                        self.tableWidget.setItem(self.rowcount, 2, item2)

                        item3 = QTableWidgetItem(amount)
                        item3.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
                        self.tableWidget.setItem(self.rowcount, 3, item3)

                        print(row[0], " ", row[1], " ", row[2], " ", type(row[2]))
                    self.rowcount = self.rowcount + 1
                    self.goodsAmountInput.setText('')
                    self.goodsNumberInput.setText('')
                else:
                    QMessageBox.warning(self, "警告", "商品不存在！", QMessageBox.Yes)

    def newSolveWidget(self):
        self.solveWidget = SolveWidget(self.getTotalMoney())


    def closeEvent(self, QCloseEvent):
        self.db.db.close()
        print("结算商品窗口关闭")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    pay = PaypalGoods()
    sys.exit(app.exec_())
