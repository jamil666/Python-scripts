# This script creates users in SQLLITE database and make search on it if needed.
# This database may be used in future for users authentication.

import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def Browse_folder(self):    # This function select database file with .db extension.
        directory = QtWidgets.QFileDialog.getOpenFileName(directory="C:/", filter="*.db")
        global filepath
        filepath = directory[0]
        self.DBname_lineEdit.setText(filepath)

    def Connect_DB(self):   # This function make connection to selected database.
        try:
            self.con = sqlite3.connect(str(filepath))
            self.cur = self.con.cursor()
            self.Output_TextEdit.setPlainText("Successfully Connected to Database!")
        except sqlite3.Error as err1:
            self.Output_TextEdit.setPlainText(err1.__str__())

    def Add_User(self): # This function create user account in database

        firstname = self.FirstName_lineEdit.text()
        lastname = self.LastName_lineEdit.text()
        username = self.UserName_lineEdit.text()
        passwd = self.Password_lineEdit.text()

        try:
            # Create new "Users" table if it is not exist.
            self.cur.execute("""CREATE TABLE IF NOT EXISTS Users ('FirstName', 'LastName', 'Username', 'Password')""")
            # Add new user information to database "Users" table.
            self.cur.execute("INSERT INTO Users ('FirstName', 'LastName', 'Username', 'Password') "
                         "VALUES ('%s', '%s', '%s', '%s')" %(firstname, lastname, username, passwd))
            self.con.commit()

            self.Output_TextEdit.setPlainText("User Successfully Created!")
        except sqlite3.Error as err2:
            self.Output_TextEdit.setPlainText(err2.__str__())

    def Search(self):   # This function search information in 'Firstname' column with 'search_input', provided by user.

        search_input = str(self.Search_lineEdit.text()).title()

        try:
            self.cur.execute(("SELECT * FROM Users WHERE FirstName = ?"), (search_input,))

            result = self.cur.fetchall()

            for x in result:
                print("Firstname: " + x[0], "Lastname: " + x[1], "Username: " + x[2], sep='\n')
                F = "Firstname: " + x[0]
                L = "Lastname: " + x[1]
                U = "Username: " + x[2]

                self.Output_TextEdit.appendPlainText("*" * 10)
                self.Output_TextEdit.appendPlainText(F.__str__())
                self.Output_TextEdit.appendPlainText(L.__str__())
                self.Output_TextEdit.appendPlainText(U.__str__())
        except:
            self.Output_TextEdit.setPlainText(sqlite3.IntegrityError)   # Show error on screen if username already exist.

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(465, 307)
        MainWindow.setMinimumSize(QtCore.QSize(465, 307))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.ShortCut = QtWidgets.QShortcut(self.centralwidget)
        self.ShortCut.setObjectName("Enter Shortcut to SearchButton")
        self.ShortCut.setKey(0x01000004)  # Enter key for Search function
        self.ShortCut.activated.connect(self.Search)

        self.DBname_label = QtWidgets.QLabel(self.centralwidget)
        self.DBname_label.setObjectName("DBname_label")
        self.gridLayout.addWidget(self.DBname_label, 0, 0, 1, 1)

        self.DBname_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.DBname_lineEdit.setObjectName("DBname_lineEdit")
        self.gridLayout.addWidget(self.DBname_lineEdit, 1, 0, 1, 1)

        self.Browse_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Browse_Button.setObjectName("Browse_Button")
        self.gridLayout.addWidget(self.Browse_Button, 1, 1, 1, 1)
        self.Browse_Button.clicked.connect(self.Browse_folder)

        self.Connect_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Connect_Button.setObjectName("Connect_Button")
        self.gridLayout.addWidget(self.Connect_Button, 1, 2, 1, 1)
        self.Connect_Button.clicked.connect(self.Connect_DB)

        self.FirstName_label = QtWidgets.QLabel(self.centralwidget)
        self.FirstName_label.setObjectName("FirstName_label")
        self.gridLayout.addWidget(self.FirstName_label, 2, 0, 1, 1)

        self.FirstName_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.FirstName_lineEdit.setObjectName("FirstName_lineEdit")
        self.gridLayout.addWidget(self.FirstName_lineEdit, 3, 0, 1, 1)


        self.Output_TextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Output_TextEdit.setObjectName("Output_TextEdit")
        self.gridLayout.addWidget(self.Output_TextEdit, 3, 1, 7, 2)

        self.LastName_label = QtWidgets.QLabel(self.centralwidget)
        self.LastName_label.setObjectName("LastName_label")
        self.gridLayout.addWidget(self.LastName_label, 4, 0, 1, 1)

        self.LastName_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.LastName_lineEdit.setObjectName("LastName_lineEdit")
        self.gridLayout.addWidget(self.LastName_lineEdit, 5, 0, 1, 1)

        self.UserName_label = QtWidgets.QLabel(self.centralwidget)
        self.UserName_label.setObjectName("UserName_label")
        self.gridLayout.addWidget(self.UserName_label, 6, 0, 1, 1)

        self.UserName_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.UserName_lineEdit.setObjectName("UserName_lineEdit")
        self.gridLayout.addWidget(self.UserName_lineEdit, 7, 0, 1, 1)

        self.Password_label = QtWidgets.QLabel(self.centralwidget)
        self.Password_label.setObjectName("Password_label")
        self.gridLayout.addWidget(self.Password_label, 8, 0, 1, 1)

        self.Password_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Password_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password_lineEdit.setObjectName("Password_lineEdit")
        self.gridLayout.addWidget(self.Password_lineEdit, 9, 0, 1, 1)

        self.Create_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Create_Button.setObjectName("Create_Button")
        self.gridLayout.addWidget(self.Create_Button, 10, 0, 1, 1)
        self.Create_Button.clicked.connect(self.Add_User)

        self.Search_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Search_lineEdit.setObjectName("Search_lineEdit")
        self.gridLayout.addWidget(self.Search_lineEdit, 10, 1, 1, 1)

        self.Search_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Search_Button.setObjectName("Search_Button")
        self.gridLayout.addWidget(self.Search_Button, 10, 2, 1, 1)
        self.Search_Button.clicked.connect(self.Search)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Developed by Jamil Kerimov")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SQLLite3 DataBase Manager"))
        self.DBname_label.setText(_translate("MainWindow", "DataBase Name"))
        self.Browse_Button.setText(_translate("MainWindow", "Browse"))
        self.Connect_Button.setText(_translate("MainWindow", "Connect"))
        self.FirstName_label.setText(_translate("MainWindow", "FirstName"))
        self.LastName_label.setText(_translate("MainWindow", "LastName"))
        self.UserName_label.setText(_translate("MainWindow", "UserName"))
        self.Password_label.setText(_translate("MainWindow", "Password"))
        self.Create_Button.setText(_translate("MainWindow", "Create"))
        self.Search_Button.setText(_translate("MainWindow", "Search"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
