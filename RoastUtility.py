# from PyQt5.QtWidgets import (QWidget, QLabel,
#     QComboBox, QApplication, QMainWindow)

from PyQt5 import QtCore, QtGui, QtWidgets



# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QComboBox, QLabel

import coffeeMenu as cm
import RMPasteData as pd
import show_coffee as sc

from RMUtility import Ui_MainWindow


class MyWindow(Ui_MainWindow):
    '''
    Inherit from class created by Qt designer in the file RMUtility2
    The critical part is in the __init__ method (also known as a constructor)
     below. You usually see it as
     super().__init__() which would call the __init__ method of the parent
     class however Qt Designer doesn't provide an __init__. It provides the
     setupUi method instead.
    '''
    def __init__(self):
        # super(MyWindow)
        super().setupUi(MainWindow)

    def __str__(self):
        return "In __str__ method of MyWindow class"

    def setupUi(self, MainWindow):
        print("In local setupUI")
        self.coffeeButton.clicked.connect(self.coffeeMenu)
        self.pasteDataButton.clicked.connect(self.pasteData)
        self.pushButtonCheckMenu.clicked.connect(self.showCoffee)
        self.actionQuit.triggered.connect(MainWindow.close)
        self.coffeeComboBox.setObjectName("MycoffeeComboBox")
        self.coffeeComboBox.addItems(["Brazil", "Burundi", "Brazil", "Costa Rica", "Ethiopia", "India", "Java"])
        # self.coffeeComboBox.addItem("Brazil")
        # self.coffeeComboBox.addItem("Burundi")
        # self.coffeeComboBox.addItem("Brazil")
        # self.coffeeComboBox.addItem("Costa Rica")
        # self.coffeeComboBox.addItem("Ethiopia")
        # self.coffeeComboBox.addItem("Java")
        self.coffeeComboBox.activated[str].connect(self.onActivated)

    def onActivated(self, text):

        self.coffeeLabel.setText(text)
        self.coffeeLabel.adjustSize()

    def coffeeMenu(self):
        print("In coffeeMenu - local")
        debug = False
        roastmaster_db = 'C:/Users/kor/Dropbox/Apps/Roastmaster/Kor Database.sqlite'
        # roastmaster_db = 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite'
        cm.check_db(roastmaster_db)
        cm.show_coffee_list(debug)
        cm.create_report()

    def pasteData(self):
        print("In pastData - local")
        debug = False
        roastmaster_db = 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite'
        # roastmaster_db = 'C:/Users/kiley_000/Dropbox/Apps/Roastmaster/My Database.sqlite'
        pd.check_db(roastmaster_db)
        pd.show_coffee_list()
        pd.create_report()

    def showCoffee(self):
        print("In pastData - local")
        debug = False
        roastmaster_db = 'c:/users/kor/dropbox/apps/roastmaster/Kor Database.sqlite'
        # roastmaster_db = 'C:/Users/kiley_000/Dropbox/Apps/Roastmaster/My Database.sqlite'
        sc.check_db(roastmaster_db)
        sc.show_coffee_list()
        sc.create_report()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MyWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())