import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# 商品管理类
from Main.Goods.insertGoods import InsertGoods
from Main.Goods.selectGoods import SelectGoods
from Main.Goods.updateGoods import UpdateGoods
from Main.Goods.deleteGoods import DeleteGoods

# 商品结算类
from Main.JieSuan.paypalGoods import PaypalGoods

# 会员管理类
from Main.Persons.selectPersons import SelectPersons
from Main.Persons.updatePersons import UpdatePersons
from Main.Persons.insertPersons import InsertPersons
from Main.Persons.deletePersons import DeletePersons



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        menuBar = self.menuBar()

        # 商品管理菜单
        goodsMannage = menuBar.addMenu('&商品管理')
        self.goodsMannageItem(goodsMannage)

        # 会员管理菜单
        personsManage = menuBar.addMenu('&会员管理')
        self.personManageItem(personsManage)

        # 商品结算
        settleGoodsManage = menuBar.addMenu('&商品结算')
        self.settleGoodsManageItem(settleGoodsManage)

        helpManage = menuBar.addMenu("&帮助")
        self.helpManageItem(helpManage)

        # 设置背景图片
        self.setGeometry(300, 300, 630, 403)
        self.setWindowTitle("超市导购")
        self.setWindowIcon(QIcon("1.jpg"))
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("33.jpg")))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        self.show()

    def helpManageItem(self,helpManage):
        aboutUsAction = QAction(QIcon("select.png"), "&关于", self)
        aboutUsAction.setShortcut('Ctrl+Shift+A')
        aboutUsAction.triggered.connect(self.gotoGithub)

        checkUpdateAction = QAction(QIcon("select.png"), "&检查更新", self)
        checkUpdateAction.setShortcut('Ctrl+Shift+U')
        checkUpdateAction.triggered.connect(self.checkUpdate)

        contactUsAction = QAction(QIcon("select.png"), "&问题反馈", self)
        contactUsAction.setShortcut('Ctrl+Shift+Q')
        contactUsAction.triggered.connect(self.gotoGithub)

        helpManage.addAction(aboutUsAction)
        helpManage.addAction(contactUsAction)
        helpManage.addAction(checkUpdateAction)

    def gotoGithub(self):
        QDesktopServices.openUrl(QUrl("https://www.baidu.com"))

    def checkUpdate(self):
        QMessageBox.information(self,"提示","您已是最新的版本1.1",QMessageBox.Yes)


    def personManageItem(self,personsManage):
        # 弹出查询会员界面
        selectPersonsAction = QAction(QIcon("select.png"), "&查询会员", self)
        selectPersonsAction.setShortcut('Shift+F')
        selectPersonsAction.triggered.connect(self.newSelectPersonsWidget)

        # 弹出添加会员界面
        insertPersonsAction = QAction(QIcon('add.png'), '&添加会员', self)
        insertPersonsAction.setShortcut('Shift+A')
        insertPersonsAction.triggered.connect(self.newInsertPersonsWidget)

        # 弹出更新商品界面
        updatePersonsAction = QAction(QIcon("update.png"), "&更新会员", self)
        updatePersonsAction.setShortcut('Shift+U')
        updatePersonsAction.triggered.connect(self.newUpdatePersonsWidget)

        # 弹出删除商品界面
        deletePersonsAction = QAction(QIcon("delete.png"), "&删除会员", self)
        deletePersonsAction.setShortcut('Shift+D')
        deletePersonsAction.triggered.connect(self.newDeletePersonsWidget)

        personsManage.addAction(selectPersonsAction)
        personsManage.addAction(insertPersonsAction)
        personsManage.addAction(updatePersonsAction)
        personsManage.addAction(deletePersonsAction)

    def newSelectPersonsWidget(self):
        self.newSelectPersonsWidget = SelectPersons()

    def newInsertPersonsWidget(self):
        self.newInsertPersonsWidget = InsertPersons()

    def newUpdatePersonsWidget(self):
        self.newUpdatePersonsWidget = UpdatePersons()

    def newDeletePersonsWidget(self):
        self.newDeletePersonsWidget = DeletePersons()


    def settleGoodsManageItem(self,settleGoodsManage):
        paypalGoodsAction = QAction(QIcon("select.png"), "&收付款", self)
        paypalGoodsAction.setShortcut('Ctrl+P')
        paypalGoodsAction.triggered.connect(self.newPaypalGoodsWidget)
        settleGoodsManage.addAction(paypalGoodsAction)

    def newPaypalGoodsWidget(self):
        self.childPaypalGoodsWidget = PaypalGoods()


    def goodsMannageItem(self,goodsMannage):

        # 弹出查询商品界面
        selectGoodsAction = QAction(QIcon("select.png"), "&查询商品", self)
        selectGoodsAction.setShortcut('Ctrl+F')
        selectGoodsAction.triggered.connect(self.newSelectGoodsWidget)

        # 弹出添加商品界面
        insertGoodsAction = QAction(QIcon('add.png'), '&添加商品', self)
        insertGoodsAction.setShortcut('Ctrl+A')
        insertGoodsAction.triggered.connect(self.newInsertGoodsWidget)


        # 弹出更新商品界面
        updateGoodsAction = QAction(QIcon("update.png"), "&更新商品", self)
        updateGoodsAction.setShortcut('Ctrl+U')
        updateGoodsAction.triggered.connect(self.newUpdateGoodsWidget)

        # 弹出删除商品界面
        deleteGoodsAction = QAction(QIcon("delete.png"), "&删除商品", self)
        deleteGoodsAction.setShortcut('Ctrl+D')
        deleteGoodsAction.triggered.connect(self.newDeleteGoodsWidget)

        goodsMannage.addAction(selectGoodsAction)
        goodsMannage.addAction(insertGoodsAction)
        goodsMannage.addAction(updateGoodsAction)
        goodsMannage.addAction(deleteGoodsAction)

    def newInsertGoodsWidget(self):
        self.childAddGoodsWidget = InsertGoods()

    def newSelectGoodsWidget(self):
        self.childSelectGoodsWidget = SelectGoods()

    def newUpdateGoodsWidget(self):
        self.childUpdateGoodsWidget = UpdateGoods()

    def newDeleteGoodsWidget(self):
        self.childDeleteGoodsWidget = DeleteGoods()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())

