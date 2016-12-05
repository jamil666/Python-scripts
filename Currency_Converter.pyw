from bs4 import BeautifulSoup
import urllib.request
from PyQt5 import QtCore, QtGui, QtWidgets

url = 'http://en.cbar.az/other/azn-rates'

def get_html(url):  # This function connects to web site

    response = urllib.request.urlopen(url)
    return response.read()

soup = BeautifulSoup(get_html(url), 'html5lib')  # Create variable for soup

table1 = soup.find_all("td", class_ = "rate")   # Select table with currency

usd = table1[0].text    # Find USD field in table
usd = float(usd)

euro = table1[1].text   # Find Euro field in table
euro = float(euro)

gbp = table1[16].text   # Find GBP field in table
gbp = float(gbp)

################################################## Application #################################################

class Ui_MainWindow(object):

    def swap(self):   # This function swap currency and recalculate it
        current_value = self.comboBox1.currentText()
        self.comboBox1.setCurrentText(self.comboBox2.currentText())
        self.comboBox2.setCurrentText(current_value)
        self.calculate()

    def calculate(self):    # This function calculate currency
        if self.comboBox1.currentText() == "AZN" and self.comboBox2.currentText() == "USD":
            x = int(self.lineEdit1.text()) / usd
            self.lineEdit2.setText(str(round(x, 4)))    # Округляет до 4 знака после запятой

        if self.comboBox1.currentText() == "USD" and self.comboBox2.currentText() == "AZN":
            x = int(self.lineEdit1.text()) * usd
            self.lineEdit2.setText(str(round(x, 4)))    # Округляет до 4 знака после запятой

        if self.comboBox1.currentText() == "AZN" and self.comboBox2.currentText() == "GBP":
            x = int(self.lineEdit1.text()) / gbp
            self.lineEdit2.setText(str(round(x, 4)))    # Округляет до 4 знака после запятой

        if self.comboBox1.currentText() == "GBP" and self.comboBox2.currentText() == "AZN":
            x = int(self.lineEdit1.text()) * gbp
            self.lineEdit2.setText(str(round(x, 4)))    # Округляет до 4 знака после запятой

        if self.comboBox1.currentText() == "AZN" and self.comboBox2.currentText() == "Euro":
            x = int(self.lineEdit1.text()) / euro
            self.lineEdit2.setText(str(round(x, 4)))    # Округляет до 4 знака после запятой

        if self.comboBox1.currentText() == "Euro" and self.comboBox2.currentText() == "AZN":
            x = int(self.lineEdit1.text()) * euro
            self.lineEdit2.setText(str(round(x, 4)))    # Округляет до 4 знака после запятой

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(243, 116)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("money.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.comboBox1 = QtWidgets.QComboBox(self.centralwidget)    # Left combobox
        self.comboBox1.setObjectName("comboBox1")
        self.gridLayout.addWidget(self.comboBox1, 0, 0, 1, 1)
        self.comboBox1.addItems(["AZN", "USD", "GBP", "Euro"])

        self.swapButton = QtWidgets.QPushButton(self.centralwidget)     # Swap button
        self.swapButton.setObjectName("revertButton")
        self.gridLayout.addWidget(self.swapButton, 0, 1, 1, 2)
        self.swapButton.clicked.connect(self.swap)

        self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)    # Right combobox
        self.comboBox2.setObjectName("comboBox2")
        self.gridLayout.addWidget(self.comboBox2, 0, 3, 1, 1)
        self.comboBox2.addItems(["AZN", "USD", "GBP", "Euro"])

        self.lineEdit1 = QtWidgets.QLineEdit(self.centralwidget)    # Left field
        self.lineEdit1.setObjectName("lineEdit1")
        self.gridLayout.addWidget(self.lineEdit1, 1, 0, 1, 2)

        self.lineEdit2 = QtWidgets.QLineEdit(self.centralwidget)    # Right field
        self.lineEdit2.setObjectName("lineEdit2")
        self.gridLayout.addWidget(self.lineEdit2, 1, 2, 1, 2)

        self.Button = QtWidgets.QPushButton(self.centralwidget)     # Convert button
        self.Button.setObjectName("Button")
        self.gridLayout.addWidget(self.Button, 2, 0, 1, 4)
        self.Button.clicked.connect(self.calculate)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Developed by Jamil Kerimov")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Конвертер валют"))
        self.swapButton.setText(_translate("MainWindow", "<>"))
        self.Button.setText(_translate("MainWindow", "Convert"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
