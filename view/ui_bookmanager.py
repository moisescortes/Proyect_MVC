# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BookManager.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BookManager(object):
    def setupUi(self, BookManager):
        BookManager.setObjectName("BookManager")
        BookManager.resize(737, 397)
        self.table_books = QtWidgets.QTableWidget(BookManager)
        self.table_books.setGeometry(QtCore.QRect(260, 30, 391, 201))
        self.table_books.setObjectName("table_books")
        self.table_books.setColumnCount(0)
        self.table_books.setRowCount(0)
        self.widget = QtWidgets.QWidget(BookManager)
        self.widget.setGeometry(QtCore.QRect(260, 270, 395, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_search = QtWidgets.QPushButton(self.widget)
        self.btn_search.setObjectName("btn_search")
        self.horizontalLayout.addWidget(self.btn_search)
        self.btn_add = QtWidgets.QPushButton(self.widget)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.btn_update = QtWidgets.QPushButton(self.widget)
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout.addWidget(self.btn_update)
        self.btn_delete = QtWidgets.QPushButton(self.widget)
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout.addWidget(self.btn_delete)
        self.widget1 = QtWidgets.QWidget(BookManager)
        self.widget1.setGeometry(QtCore.QRect(40, 50, 139, 140))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txt_book_id = QtWidgets.QLineEdit(self.widget1)
        self.txt_book_id.setObjectName("txt_book_id")
        self.verticalLayout.addWidget(self.txt_book_id)
        self.txt_title = QtWidgets.QLineEdit(self.widget1)
        self.txt_title.setObjectName("txt_title")
        self.verticalLayout.addWidget(self.txt_title)
        self.txt_author = QtWidgets.QLineEdit(self.widget1)
        self.txt_author.setObjectName("txt_author")
        self.verticalLayout.addWidget(self.txt_author)
        self.txt_genre = QtWidgets.QLineEdit(self.widget1)
        self.txt_genre.setObjectName("txt_genre")
        self.verticalLayout.addWidget(self.txt_genre)
        self.cmb_status = QtWidgets.QComboBox(self.widget1)
        self.cmb_status.setObjectName("cmb_status")
        self.cmb_status.addItem("")
        self.cmb_status.addItem("")
        self.verticalLayout.addWidget(self.cmb_status)

        self.retranslateUi(BookManager)
        QtCore.QMetaObject.connectSlotsByName(BookManager)

    def retranslateUi(self, BookManager):
        _translate = QtCore.QCoreApplication.translate
        BookManager.setWindowTitle(_translate("BookManager", "Form"))
        self.btn_search.setText(_translate("BookManager", "Buscar"))
        self.btn_add.setText(_translate("BookManager", "Agregar"))
        self.btn_update.setText(_translate("BookManager", "Actualizar"))
        self.btn_delete.setText(_translate("BookManager", "Eliminar"))
        self.txt_book_id.setText(_translate("BookManager", "ID del libro"))
        self.txt_title.setText(_translate("BookManager", "Título"))
        self.txt_author.setText(_translate("BookManager", "Autor"))
        self.txt_genre.setText(_translate("BookManager", "Género"))
        self.cmb_status.setItemText(0, _translate("BookManager", "Disponible"))
        self.cmb_status.setItemText(1, _translate("BookManager", "Prestado"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BookManager = QtWidgets.QWidget()
    ui = Ui_BookManager()
    ui.setupUi(BookManager)
    BookManager.show()
    sys.exit(app.exec_())
