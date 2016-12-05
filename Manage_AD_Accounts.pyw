from ldap3 import Server, Connection, ALL, Tls, MODIFY_REPLACE
import ssl
from PyQt5 import QtCore, QtGui, QtWidgets

tls_configuration = Tls(validate=ssl.CERT_REQUIRED, version=ssl.PROTOCOL_TLSv1_2)   # Using TLS in connection.

# This function used for connection to Active Directory with provided login and password.


class Ui_MainWindow(object):
    def ldap_bind(self):

        domain = 'domain.com'   # Domain name should be changed
        username = self.LoginInput.text() + "@" + domain

        passwd = self.PasswordInput.text()

        try:
            s = Server(domain, port=636, get_info=ALL, use_ssl=True, tls=tls_configuration)
            global c
            c = Connection(s, user = username, password = passwd, check_names=True, lazy=False,
                           raise_exceptions=True, )
            c.open()
            c.bind()

            self.Output.appendPlainText("User %s has been successfully connected to Active Directory!" %username)
            self.Output.appendPlainText("*" * 30)
        except:
            self.Output.appendPlainText("Invalid credentials! Please try again!")
            self.Output.appendPlainText("*" * 30)

    def adsearch(self):  # This function show information about user from Active Directory.

        c.search("dc = DOMAIN, dc = COM",   # Domain name should be changed
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

        c.search("dc = DOMAIN, dc = COM",   # Domain name should be changed
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
                    self.Output.appendPlainText(str("*" * 35))
        else:
            self.Output.appendPlainText("User not found!")
            self.Output.appendPlainText(str("*" * 35))

    def reset_password(self):  # This function reset user password to 123456789F!

        c.search("dc = DOMAIN, dc = COM",   # Domain name should be changed
                 search_filter="(sAMAccountName = %s*)" % self.UserInput.text(),
                 search_scope="SUBTREE",
                 attributes=['distinguishedName', 'displayName', 'pwdLastSet'])
        list = c.entries

        for x in list:
            c.extend.microsoft.modify_password("%s" % x['distinguishedName'], new_password="123456789F!") # Password may be changed
            self.Output.appendPlainText(str("Password for %s was changed successfully!" %x['displayName']))

            self.Output.appendPlainText("*" * 35)

    def password_reset_UMCP(self):  # This function reset user password to 123456789F! User Must Change Password.

        c.search("dc = DOMAIN, dc = COM",   # Domain name should be changed
                 search_filter="(sAMAccountName = %s*)" % self.UserInput.text(),
                 search_scope="SUBTREE",
                 attributes=['distinguishedName', 'displayName', 'pwdLastSet'])
        list = c.entries

        for x in list:
            c.extend.microsoft.modify_password("%s" % x['distinguishedName'], new_password="123456789F!")   # Password may be changed
            c.modify("%s" % x['distinguishedName'], {'pwdLastSet': [(MODIFY_REPLACE, ['0'])]})
            self.Output.appendPlainText(str("Password for %s was changed successfully!" %x['displayName']))
            self.Output.appendPlainText("User must change password at next logon!")
            self.Output.appendPlainText("*" * 35)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560, 248)
        MainWindow.setMinimumSize(QtCore.QSize(480, 212))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.Username_label = QtWidgets.QLabel(self.centralwidget)
        self.Username_label.setToolTip("")
        self.Username_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Username_label.setObjectName("Username_label")
        self.gridLayout.addWidget(self.Username_label, 0, 0, 1, 1)

        self.Password_label = QtWidgets.QLabel(self.centralwidget)
        self.Password_label.setTextFormat(QtCore.Qt.AutoText)
        self.Password_label.setScaledContents(False)
        self.Password_label.setObjectName("Password_label")
        self.gridLayout.addWidget(self.Password_label, 0, 1, 1, 1)

        self.Output = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Output.setFont(font)
        self.Output.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Output.setObjectName("Output")
        self.gridLayout.addWidget(self.Output, 0, 2, 8, 1)

        self.LoginInput = QtWidgets.QLineEdit(self.centralwidget)
        self.LoginInput.setText("")
        self.LoginInput.setFrame(True)
        self.LoginInput.setObjectName("LoginInput")
        self.gridLayout.addWidget(self.LoginInput, 1, 0, 1, 1)

        self.PasswordInput = QtWidgets.QLineEdit(self.centralwidget)
        self.PasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordInput.setObjectName("PasswordInput")
        self.gridLayout.addWidget(self.PasswordInput, 1, 1, 1, 1)

        self.LoginButton = QtWidgets.QPushButton(self.centralwidget)
        self.LoginButton.setObjectName("LoginButton")
        self.gridLayout.addWidget(self.LoginButton, 2, 0, 1, 2)
        self.LoginButton.clicked.connect(self.ldap_bind)

        self.ShortCut = QtWidgets.QShortcut(self.centralwidget)
        self.ShortCut.setObjectName("Enter Shortcut to LoginButton")
        self.ShortCut.setKey(0x01000004)    # Enter key connected to ldap_bind function
        self.ShortCut.activated.connect(self.ldap_bind)

        self.UserInput = QtWidgets.QLineEdit(self.centralwidget)
        self.UserInput.setObjectName("UserInput")
        self.gridLayout.addWidget(self.UserInput, 3, 0, 1, 2)

        self.UnlockButton = QtWidgets.QPushButton(self.centralwidget)
        self.UnlockButton.setObjectName("UnlockButton")
        self.gridLayout.addWidget(self.UnlockButton, 4, 0, 1, 2)
        self.UnlockButton.clicked.connect(self.unlock_account)

        self.ResetButton = QtWidgets.QPushButton(self.centralwidget)
        self.ResetButton.setObjectName("ResetButton")
        self.gridLayout.addWidget(self.ResetButton, 5, 0, 1, 2)
        self.ResetButton.clicked.connect(self.password_reset_UMCP)

        self.ResetButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.ResetButton_2.setObjectName("ResetButton_2")
        self.gridLayout.addWidget(self.ResetButton_2, 6, 0, 1, 2)
        self.ResetButton_2.clicked.connect(self.reset_password)

        self.InfoButton = QtWidgets.QPushButton(self.centralwidget)
        self.InfoButton.setObjectName("InfoButton")
        self.gridLayout.addWidget(self.InfoButton, 7, 0, 1, 2)
        self.InfoButton.clicked.connect(self.adsearch)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AD Account Management Tool"))
        self.Username_label.setText(_translate("MainWindow", "Username"))
        self.Password_label.setText(_translate("MainWindow", "Password"))
        self.LoginInput.setToolTip(_translate("MainWindow", "Username"))
        self.PasswordInput.setToolTip(_translate("MainWindow", "Password"))
        self.LoginButton.setText(_translate("MainWindow", "Login"))
        self.UserInput.setToolTip(_translate("MainWindow", "Account Name"))
        self.UnlockButton.setText(_translate("MainWindow", "Unlock Account"))
        self.ResetButton.setToolTip(_translate("MainWindow", "Password will be changed to 123456789F! User Must Change Password!"))
        self.ResetButton.setText(_translate("MainWindow", "Reset Password to Default. UMCP"))
        self.ResetButton_2.setToolTip(_translate("MainWindow", "Password will be changed to 123456789F!"))
        self.ResetButton_2.setText(_translate("MainWindow", "Reset Password to Default."))
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
