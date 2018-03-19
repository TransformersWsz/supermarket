from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from DAO.select import Select

class SelectGoods(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Select()
        self.cursor = self.db.connectdb()

        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(200, 200, 1200, 600)
        self.setWindowTitle("查询商品")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)


        # 初始化查询框
        self.searchInput = QLineEdit(self)
        self.searchInput.setGeometry(425, 90, 300, 30)
        self.searchInput.setPlaceholderText("请输入商品编号")
        self.searchInput.setStyleSheet("border-radius: 8px; background-color: #F8F8FF;border-color: red;border-style: solid")
        # 初始化查询按钮
        self.searchBtn = QPushButton(self)
        self.searchBtn.setIcon(QIcon('search.png'))
        self.searchBtn.setGeometry(730,85,45,45)
        self.searchBtn.setStyleSheet("background-color:transparent;border-width: 0px")
        self.searchBtn.clicked.connect(self.searchByNumber)


        # 初始化表格
        self.tableWidget = QTableWidget(self)
        self.tableWidget.move(0, 200)
        self.tableWidget.resize(1200, 397)
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setHorizontalHeaderLabels(["商品编号", "名称", "数量", "单位", "价格","保质期","联系电话","生产地址","生产日期","生产厂家","备注"])
        self.tableWidget.verticalHeader().setDefaultSectionSize(38)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        sql = "select number, name, amount,unit, price,life,telephone,produceaddress,producedate,producer,remark from goods"
        counts, results = self.db.select(self.cursor,sql,())

        self.tableWidget.setRowCount(counts)

        i = 0
        for row in results:
            number = row[0]
            name = row[1]
            amount = row[2]
            unit = row[3]
            price = row[4]
            life = row[5]
            telephone = row[6]
            produceaddress = row[7]
            producedate = row[8]
            producer = row[9]
            remark = row[10]
            print(number, " ", name, " ", amount, " ",unit," ", price," ",life," ",telephone," ",produceaddress," ",producedate," ",producer," ",remark)

            # item = QTableWidgetItem(str(number))
            # item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            # 获取某个单元格
            # item = self.tableWidget.itemAt(i,0)
            # print(item.text())


            self.tableWidget.setItem(i, 0, QTableWidgetItem(self.turn(str(number))))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(name)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(amount)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(unit)))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(price)))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(life)))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(self.turn(telephone)))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(self.turn(produceaddress)))
            self.tableWidget.setItem(i, 8, QTableWidgetItem(self.turn(str(producedate))))
            self.tableWidget.setItem(i, 9, QTableWidgetItem(self.turn(producer)))
            self.tableWidget.setItem(i, 10, QTableWidgetItem(self.turn(remark)))
            i = i + 1

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 初始化清空按钮
        # self.clearBtn = QPushButton("clear", self)
        # self.clearBtn.setGeometry(100, 100, 50, 30)
        # self.clearBtn.clicked.connect(self.clearTable)


    def searchByNumber(self):
        inputText = self.searchInput.text()
        if inputText == '':
            print("为空")
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            self.tableWidget.resize(1200, 27)
        else:
            searchsql = "select number, name, amount,unit, price,life,telephone,produceaddress,producedate,producer,remark from goods where number = %s"
            values = (inputText)
            searchCounts, searchResults = self.db.select(self.cursor, searchsql,values)
            self.tableWidget.setRowCount(searchCounts)
            self.tableWidget.resize(1200, 38 * (searchCounts + 1) - 10)

            i = 0
            for row in searchResults:
                number = row[0]
                name = row[1]
                amount = row[2]
                unit = row[3]
                price = row[4]
                life = row[5]
                telephone = row[6]
                produceaddress = row[7]
                producedate = row[8]
                producer = row[9]
                remark = row[10]
                print(number, " ", name, " ", amount, " ", unit, " ", price, " ", life, " ", telephone, " ", produceaddress,
                      " ", producedate, " ", producer, " ", remark)

                self.tableWidget.setItem(i, 0, QTableWidgetItem(self.turn(str(number))))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(self.turn(str(name))))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(self.turn(str(amount))))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(self.turn(str(unit))))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(self.turn(str(price))))
                self.tableWidget.setItem(i, 5, QTableWidgetItem(self.turn(str(life))))
                self.tableWidget.setItem(i, 6, QTableWidgetItem(self.turn(telephone)))
                self.tableWidget.setItem(i, 7, QTableWidgetItem(self.turn(produceaddress)))
                self.tableWidget.setItem(i, 8, QTableWidgetItem(self.turn(str(producedate))))
                self.tableWidget.setItem(i, 9, QTableWidgetItem(self.turn(producer)))
                self.tableWidget.setItem(i, 10, QTableWidgetItem(self.turn(remark)))
                i = i + 1

    def turn(self,value):
        if value == None:
            value = ''
        return value


    def clearTable(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.resize(1200,27)

    def closeEvent(self, QCloseEvent):
        self.db.db.close()
        print("查询商品窗口关闭")

