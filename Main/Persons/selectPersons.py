from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

from DAO.select import Select

class SelectPersons(QWidget):
    def __init__(self):
        super().__init__()

        self.db = Select()
        self.cursor = self.db.connectdb()

        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("查询会员")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # 初始化查询框
        self.searchInput = QLineEdit(self)
        self.searchInput.setGeometry(250, 90, 280, 30)
        self.searchInput.setPlaceholderText("请输入会员账号")
        self.searchInput.setStyleSheet("border-radius: 8px; background-color: #F8F8FF;border-color: red;border-style: solid")
        # 初始化查询按钮
        self.searchBtn = QPushButton(self)
        self.searchBtn.setIcon(QIcon('search.png'))
        self.searchBtn.setGeometry(530, 90, 45, 45)
        self.searchBtn.setStyleSheet("background-color:transparent;border-width: 0px")
        self.searchBtn.clicked.connect(self.searchByNumber)


        # 初始化表格
        self.tableWidget = QTableWidget(self)
        self.tableWidget.move(0, 200)
        self.tableWidget.resize(800, 300)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(
            ["帐号", "姓名", "联系电话","总消费金额","会员等级"])
        self.tableWidget.verticalHeader().setDefaultSectionSize(38)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        sql = "select number,name,telephone,totalconsumemoney,level from persons"
        counts,results = self.db.select(self.cursor,sql,())
        self.tableWidget.setRowCount(counts)

        i = 0
        for row in results:
            number = row[0]
            name = row[1]
            telephone = row[2]
            totalconsumemoney = row[3]
            level = row[4]
            print(number," ",name," ",telephone," ",totalconsumemoney," ",level)

            item0 = QTableWidgetItem(str(number))
            item0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 0, item0)

            item1 = QTableWidgetItem(str(name))
            item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 1, item1)

            item2 = QTableWidgetItem(str(telephone))
            item2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 2, item2)

            item3 = QTableWidgetItem(self.turn(str(totalconsumemoney)))
            item3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 3, item3)

            item4 = QTableWidgetItem(str(level))
            item4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(i, 4, item4)

            i = i + 1

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)



    def searchByNumber(self):
        inputText = self.searchInput.text()
        if inputText == '':
            print("为空")
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)
            self.tableWidget.resize(1200, 27)
        else:
            searchsql = "select number,name,telephone,totalconsumemoney,level from persons where number = %s"
            values = (inputText)
            searchCounts, searchResults = self.db.select(self.cursor, searchsql,values)
            self.tableWidget.setRowCount(searchCounts)

            i = 0
            for row in searchResults:
                number = row[0]
                name = row[1]
                telephone = row[2]
                totalconsumemoney = row[3]
                level = row[4]
                print(number, " ", name, " ", telephone, " ", totalconsumemoney, " ", level)

                item0 = QTableWidgetItem(str(number))
                item0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 0, item0)

                item1 = QTableWidgetItem(str(name))
                item1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 1, item1)

                item2 = QTableWidgetItem(str(telephone))
                item2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 2, item2)

                item3 = QTableWidgetItem(self.turn(str(totalconsumemoney)))
                item3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 3, item3)

                item4 = QTableWidgetItem(str(level))
                item4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 4, item4)

                i = i + 1

    def turn(self,value):
        if value == None:
            value = ''
        return value

    def closeEvent(self, QCloseEvent):
        self.db.db.close()
        print("查询会员窗口关闭")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     test = SelectPersons()
#     sys.exit(app.exec_())