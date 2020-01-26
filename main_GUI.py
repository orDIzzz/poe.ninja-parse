import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from GUI.GUI_1 import *
import tiers


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.SelectAllBtn.clicked.connect(self.SelectAllBtn_clicked)
        self.ui.RemoveAllBtn.clicked.connect(self.RemoveAllBtn_clicked)
        self.ui.LoadBtn.clicked.connect(self.LoadBtn_clicked)
        self.ui.SaveBtn.clicked.connect(self.SaveBtn_clicked)
        self.ui.SortBtn.clicked.connect(self.SortBtn_clicked)
        self.checkboxes = {self.ui.UniquesCheck: tiers.uniques, self.ui.UniqueMapsCheck: tiers.uni_maps,
                           self.ui.FragmentsCheck: tiers.fragments, self.ui.DivinationCheck: tiers.div_cards,
                           self.ui.FossilsCheck: tiers.fossils, self.ui.ResonatorsCheck: tiers.resonators,
                           self.ui.ScarabsCheck: tiers.scarabs, self.ui.OilsCheck: tiers.oils,
                           self.ui.IncubatorsCheck: tiers.incubators}

    def SelectAllBtn_clicked(self):
        for checkbox in self.checkboxes.keys():
            if checkbox.isChecked() is False:
                checkbox.toggle()

    def RemoveAllBtn_clicked(self):
        for checkbox in self.checkboxes.keys():
            if checkbox.isChecked() is True:
                checkbox.toggle()

    def LoadBtn_clicked(self):
        pass

    def SaveBtn_clicked(self):
        pass

    def SortBtn_clicked(self):
        for checkbox in self.checkboxes.keys():
            if checkbox.isChecked() is True:
                print(self.checkboxes[checkbox].take_bases())
                print('Группа ', self.checkboxes[checkbox])

    def mbox(self, body, title='Error'):
        dialog = QMessageBox(QMessageBox.Information, title, body)
        dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
