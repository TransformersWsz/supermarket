from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import sys
import time

from DAO.select import Select
from DAO.update import Update

class SolveWidget(QWidget):
    def __init__(self,info):
        super().__init__()
        self.info = info
        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(100,100,273,277)
        self.setWindowTitle("付款")

        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.darkCyan)
        ft = QFont()
        ft.setPointSize(15)


        totalMoneyLabel = QLabel("应付金额：",self)
        totalMoneyLabel.setGeometry(50,30,100,30)
        totalMoneyLabel.setFont(ft)
        totalMoneyLabel.setPalette(pe)

        sumMoneyLabel = QLabel(self)
        sumMoneyLabel.setGeometry(150, 30, 150, 30)
        sumMoneyLabel.setText(str(self.info[0]))
        sumMoneyLabel.setFont(ft)
        sumMoneyLabel.setPalette(pe)


        actualMoneyLabel = QLabel("实付金额：",self)
        actualMoneyLabel.setGeometry(50,80,100,30)
        actualMoneyLabel.setPalette(pe)
        actualMoneyLabel.setFont(ft)

        self.realMoneyInput = QLineEdit(self)
        self.realMoneyInput.setGeometry(150,80,100,30)
        self.realMoneyInput.setFont(ft)
        self.realMoneyInput.setPalette(pe)
        self.realMoneyInput.setStyleSheet("border-radius: 8px; background-color: #F8F8FF;border-color: red;border-style: solid")


        personNumberLabel = QLabel("会员卡号：",self)
        personNumberLabel.setGeometry(50,130,150,30)
        personNumberLabel.setPalette(pe)
        personNumberLabel.setFont(ft)

        self.personNumberInput = QLineEdit(self)
        self.personNumberInput.setGeometry(150,130,100,30)
        self.personNumberInput.setFont(ft)
        self.personNumberInput.setPalette(pe)
        self.personNumberInput.setStyleSheet("border-radius: 8px; background-color: #F8F8FF;border-color: red;border-style: solid")

        okBtn = QPushButton("使用会员卡支付",self)
        okBtn.setGeometry(56.5,190,160,30)
        okBtn.setStyleSheet("background-color:#63B8FF; border-width: 2px; border-radius: 3px")
        okBtn.clicked.connect(self.compare)

        okBtn1 = QPushButton("优惠支付", self)
        okBtn1.setGeometry(56.5, 240, 160, 30)
        okBtn1.setStyleSheet("background-color:#63B8FF; border-width: 2px; border-radius: 3px")
        okBtn1.clicked.connect(self.fullpay)

    def fullpay(self):
        select = Select()
        cursor = select.connectdb()
        fulldiscountsql = "select `condition`,reduce from favourable"
        counts, results = select.select(cursor, fulldiscountsql, ())
        if counts == 0:
            select.db.close()
            self.on_htmlButton_clicked()
            return
        else:
            if self.info[0] < float(results[0][0]):
                select.db.close()
                self.on_htmlButton_clicked()
                return
            else:
                previous = 0
                reduce = 0
                for row in results:
                    if self.info[0] >= row[0]:
                        previous = row[0]
                        reduce = row[1]
                    else:
                        break
                select.db.close()
                fulldiscount = self.info[0] - reduce
                self.shouldmoney = fulldiscount
                self.on_htmlButton_clicked()


    def compare(self):
        personNumber = self.personNumberInput.text()
        if personNumber == "":
            QMessageBox.warning(self,"警告","会员卡号不能为空",QMessageBox.Yes)
            return
        else:
            sql = "select level from persons where number = %s"
            values = (personNumber)
            select = Select()
            cursor = select.connectdb()
            counts,results = select.select(cursor,sql,values)

            if counts == 0:
                QMessageBox.warning(self,"错误","该会号不存在，请重新输入卡号！",QMessageBox.Yes)
                select.db.close()
                self.personNumberInput.setText("")
                return
            else:
                level = int(results[0][0])
                discount = 1 - level * 0.10

                # 会员卡结算后的优惠
                numberdiscount = self.info[0] * discount
                # 满折优惠
                select = Select()
                cursor = select.connectdb()
                fulldiscountsql = "select `condition`,reduce from favourable"
                counts,results = select.select(cursor,fulldiscountsql,())
                if counts == 0:
                    select.db.close()
                    self.on_htmlButton_clicked()
                    return
                else:
                    if self.info[0] < float(results[0][0]):
                        select.db.close()
                        self.on_htmlButton_clicked()
                        return
                    else:
                        previous = 0
                        reduce = 0
                        for row in results:
                            if self.info[0] >= row[0]:
                                previous = row[0]
                                reduce = row[1]
                            else:
                                break
                        fulldiscount = self.info[0] - reduce
                        if fulldiscount >= numberdiscount:
                            select.db.close()
                            self.on_htmlButton_clicked()
                        else:
                            select.db.close()
                            tip = "使用满%s减%s，你将支付%s元。使用会员卡优惠你将支付%s元，是否继续交易？" % (str(previous),str(reduce),str(fulldiscount),str(numberdiscount))
                            button = QMessageBox.question(self, "温馨提示", tip, QMessageBox.Ok | QMessageBox.Cancel)
                            if button == QMessageBox.Ok:
                                self.shouldmoney = numberdiscount
                                self.on_htmlButton_clicked()
                            else:
                                self.shouldmoney = fulldiscount


    def on_htmlButton_clicked(self):
        self.printer = QPrinter(QPrinter.HighResolution)
        # /* 打印预览 */
        preview = QPrintPreviewDialog(self.printer,self)
        preview.paintRequested.connect(self.printHtml)
        preview.exec_()

    def printHtml(self):
        html1 = """
                <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>小票</title>
            <style>
                body {
                    text-align: center
                }
                .box {
                    margin: 10px auto;
                    width: 1000px;
                }
            </style>
        </head>

        <body>
            <div align="center">
                <span style="font-size: 100px">苏州大学教育超市本部</span>
            </div>
            <div align="center">
                <span style="font-size: 100px">欢迎光临</span>
            </div>
            <div align="center">********************************
                <span style="font-size: 100px">交易</span>********************************</div>"""

        # 实付金额
        actualMoney = float(self.realMoneyInput.text())

        # 累计数量
        amount = 0
        origintotal = 0
        html2 = ""
        for good in self.info[1]:
            amount = good[3] + amount
            html2 = html2 + """<div style="margin-top: 10px">
        <span style="float: left; margin-left: 5%; font-size: 100px">""" + str(good[0]) + """</span>
        <span style="float: right; margin-right: 5%; font-size: 100px">""" + str(good[1]) + """</span>
    </div>

    <div class="box" style="margin-top: 10px">
        <div align="center" style="font-size: 100px">&nbsp;&nbsp;&nbsp;&nbsp;
""" + str(good[2]) + """&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; """ + str(good[3]) + """ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;""" + str(good[2] * good[3]) + """&nbsp;&nbsp;&nbsp;&nbsp;</div>
    </div>"""
            origintotal = good[2] * good[3] + origintotal


        html2 = html2 + """<div align="center" style="margin-top: 10px">---------------------------------------------------------------------------</div>
    <div style="margin:10px auto; width: 500px">
        <span style="float: left; margin-left: 5%; font-size: 100px">累计数量 : """ + str(amount) + """</span>
        <span style="float: right; margin-right: 5%; font-size: 100px">原价合计 : """ + str(origintotal) + """</span>
    </div>
    <div style="margin:10px auto; width: 1000px">
        <span style="float: left; margin-left: 5%; font-size: 100px">应付金额 : """ + str(self.shouldmoney) + """</span>
        <span style="float: right; margin-right: 5%; font-size: 100px">实付金额 : """ + str(actualMoney) + """</span>
    </div>
    <div style="margin:10px auto; width: 1000px">
        <span style="float: left; margin-left: 5%; font-size: 100px">找零 : """ + str(actualMoney - self.shouldmoney) + """</span>
        <span style="float: right; margin-right: 5%; font-size: 100px">收款机 : 002</span>
    </div>"""

        consumetime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        html3 = """<div align="center" style="margin-top: 10px;font-size: 100px">消费日期：""" + consumetime + """</div>
    <div align="center" style="margin-top: 10px">---------------------------------------------------------------------------</div>
    <div align="center" style="margin-top: 10px; font-size: 130px">谢谢惠顾，欢迎再来</div>
</body>

</html>"""
        html = html1 + html2 + html3

        textDocument = QTextDocument()
        textDocument.setHtml(html)
        textDocument.print_(self.printer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    info = (480,[("1001","可口可乐",2.5,192)])
    test = SolveWidget(info)
    sys.exit(app.exec_())


