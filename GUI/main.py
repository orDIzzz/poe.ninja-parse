import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from GUI.GUI_1 import *


class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.SelectAllBtn.clicked.connect(self.SelectAllBtn_clicked)
        self.ui.RemoveAllBtn.clicked.connect(self.RemoveAllBtn_clicked)

    def SelectAllBtn_clicked(self):
        checkboxes = (self.ui.UniquesCheck, self.ui.UniqueMapsCheck, self.ui.FragmentsCheck, self.ui.DivinationCheck,
                      self.ui.FossilsCheck, self.ui.ResonatorsCheck, self.ui.ScarabsCheck, self.ui.OilsCheck,
                      self.ui.IncubatorsCheck)
        for checkbox in checkboxes:
            if checkbox.isChecked() is False:
                checkbox.toggle()

    def RemoveAllBtn_clicked(self):
        checkboxes = (self.ui.UniquesCheck, self.ui.UniqueMapsCheck, self.ui.FragmentsCheck, self.ui.DivinationCheck,
                      self.ui.FossilsCheck, self.ui.ResonatorsCheck, self.ui.ScarabsCheck, self.ui.OilsCheck,
                      self.ui.IncubatorsCheck)
        for checkbox in checkboxes:
            if checkbox.isChecked() is True:
                checkbox.toggle()

    def mbox(self, body, title='Error'):
        dialog = QMessageBox(QMessageBox.Information, title, body)
        dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
