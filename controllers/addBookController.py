from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from views.Add_Nakama_View import Ui_Dialog
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from dbConnection.VerifyConnection import VerifyConnection

#from model.Objects.Book import Book
#from model.DAO.Add_Nakama_DAO import BookDAO

class AddNakamaController(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        print("I'm adding a new Book :D")
        self.ui = Ui_Dialog()
        # DAO instance
        self.book_dao = BookDAO()
        self.ui.setupUi(self)
        self.initializeGUI()

    # Initialize elements, for example, setting up button functionality
    def initializeGUI(self):

        self.ui.btnAddNakama.clicked.connect(self.addNakama)
        self.ui.le_Name.setStyleSheet("QLineEdit { font-family: Arial; font-size: 16px; font-style: italic; }")
        self.ui.le_Rol.setStyleSheet("QLineEdit { font-family: Arial; font-size: 16px; font-style: italic; }")
        self.ui.le_Crew.setStyleSheet("QLineEdit { font-family: Arial; font-size: 16px; font-style: italic; }")
        self.validateNumber = QRegExpValidator(QRegExp("^[0-9]+$ "), self)
        self.validateStringNoSpaces = QRegExpValidator(QRegExp("[a-zA-Zñ]+"), self)

    def addNakama(self):
        try:
            name = self.ui.le_Name.text()
            rol = self.ui.le_Rol.text()
            crew = self.ui.le_Crew.text()

            new_nakama = Nakama(name,rol,crew)  # Create Nakama object

            # Check if there is an Internet connection
            if VerifyConnection.verify_connection(self):
                # Try to add it to Firebase if there is a connection
                self.nakama_dao.add_nakama(new_nakama)

                # Check if the operation was successful
                if self.nakama_dao.nakama_ref is not None:
                    # Show confirmation if successful
                    QMessageBox.information(self, 'Confirmation', "A new Nakama has been registered ✔", QMessageBox.Ok)
                else:
                    # Show error message if it couldn't be added
                    QMessageBox.critical(self, "Error",
                                         "Cannot connect to Firebase. Check your Internet connection.",
                                         QMessageBox.Ok)
            else:
                # If there is no Internet connection, show an error message
                QMessageBox.critical(self, "Error", "No Internet connection. Please check your connection.", QMessageBox.Ok)

            self.clearFields()  # Clear fields after adding

        except Exception as e:
            # If there is an unexpected error
            print(f"❌ Error : {e}")
            QMessageBox.critical(self, "Error", "An unexpected error occurred while adding the Nakama.", QMessageBox.Ok)

    def clearFields(self):
        print("Clean Fields")
