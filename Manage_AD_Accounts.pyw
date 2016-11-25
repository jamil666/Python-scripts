from ldap3 import Server, Connection, ALL, Tls, MODIFY_REPLACE
import ssl
from PyQt5 import QtCore, QtWidgets, QtGui

tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)   # Using TLS in connection.

# This function used for connection to Active Directory with provided login and password.
def ldap_bind():
    s = Server("azerfon.az", port=636, get_info=ALL, use_ssl=True, tls=tls_configuration)
    global c
    c = Connection(s, user="domain\username", password="password", check_names=True, lazy=False,
                   raise_exceptions=True, )
    c.open()
    c.bind()

ldap_bind()

class Ui_MainWindow(object):

    def adsearch(self):  # This function show information about user from Active Directory.

        c.search("dc = azerfon, dc = az",
                 search_filter="(sAMAccountName = %s*)" % self.UserInput.text(),
                 search_scope="SUBTREE",
                 attributes=['displayName', 'employeeID', 'mail', 'title', 'department',
                             'mobile', 'UserAccountControl', 'lockoutTime'])

        list = c.entries

        for x in list:
            self.Output.appendPlainText(str("Display Name:      %s" % x['displayName']))
            self.Output.appendPlainText(str("Email:             %s" % x['mail']))
            self.Output.appendPlainText(str("Job title:         %s" % x['title']))
            self.Output.appendPlainText(str("Mobile:            %s" % x['mobile']))
            self.Output.appendPlainText(str("EmployeeID:        %s" % x['employeeID']))
            self.Output.appendPlainText(str("*" * 35))

    def unlock_account(self):  # This function unlock user account

        c.search("dc = azerfon, dc = az",
                 search_filter="(sAMAccountName = %s*)" % self.UserInput.text(),
                 search_scope="SUBTREE",
                 attributes=['distinguishedName', 'displayName', 'lockoutTime'])

        list = c.entries

        if list != []:
            for x in list:
                if x['lockoutTime'] != b'0':
                    c.modify("%s" %x['distinguishedName'], {'lockoutTime': [(MODIFY_REPLACE, ['0'])]})
                    self.Output.appendPlainText(str("User %s unlocked." %x['displayName']))
                    self.Output.appendPlainText(str("*" * 35))
                else:
                    self.Output.appendPlainText("User not locked!")
        else:
            self.Output.appendPlainText("User not found!")

    def password_reset_UMCP(self):  # This function reset user password to 123456789F! User Must Change Password.

        c.search("dc = azerfon, dc = az",
                 search_filter="(sAMAccountName = %s*)" % self.UserInput.text(),
                 search_scope="SUBTREE",
                 attributes=['distinguishedName', 'displayName', 'pwdLastSet'])
        list = c.entries

        for x in list:
            c.extend.microsoft.modify_password("%s" % x['distinguishedName'], new_password="123456789F!")
            c.modify("%s" % x['distinguishedName'], {'pwdLastSet': [(MODIFY_REPLACE, ['0'])]})
            self.Output.appendPlainText(str("Password for %s was changed successfully!" %x['displayName']))
            self.Output.appendPlainText("*" * 35)

    ############################################## Application ######################################################

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(438, 147)
        MainWindow.setMinimumSize(QtCore.QSize(438, 147))
        MainWindow.setMaximumSize(QtCore.QSize(438, 147))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("AD.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.UserInput = QtWidgets.QLineEdit(self.centralwidget)    # Input window
        self.UserInput.setObjectName("UserInput")
        self.gridLayout.addWidget(self.UserInput, 0, 0, 1, 1)

        self.Output = QtWidgets.QPlainTextEdit(self.centralwidget)  # Output window
        self.Output.setObjectName("Output")
        self.gridLayout.addWidget(self.Output, 0, 1, 4, 1)

        self.UnlockButton = QtWidgets.QPushButton(self.centralwidget)   # Unlock button
        self.UnlockButton.setObjectName("UnlockButton")
        self.gridLayout.addWidget(self.UnlockButton, 1, 0, 1, 1)
        self.UnlockButton.clicked.connect(self.unlock_account)

        self.ResetButton = QtWidgets.QPushButton(self.centralwidget)    # Reset button
        self.ResetButton.setObjectName("ResetButton")
        self.gridLayout.addWidget(self.ResetButton, 2, 0, 1, 1)
        self.ResetButton.clicked.connect(self.password_reset_UMCP)

        self.InfoButton = QtWidgets.QPushButton(self.centralwidget)     # Info button
        self.InfoButton.setObjectName("InfoButton")
        self.gridLayout.addWidget(self.InfoButton, 3, 0, 1, 1)
        self.InfoButton.clicked.connect(self.adsearch)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AD Account Management"))
        self.UnlockButton.setText(_translate("MainWindow", "Unlock Account"))
        self.ResetButton.setText(_translate("MainWindow", "Set Default Password"))
        self.InfoButton.setText(_translate("MainWindow", "Show User Info"))
        self.statusbar.showMessage("Developed by Jamil Kerimov")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
