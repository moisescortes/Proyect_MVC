import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from controllers.BookController import BookController  # Importar el controlador
from view.BookManagerApp import BookManagerApp
from view.ui_mainwindow import Ui_MainWindow  # Importar la GUI convertida

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conectar botones con funciones
        self.ui.btn_books.clicked.connect(self.open_book_manager)
        self.ui.btn_exit.clicked.connect(self.close)

    def open_book_manager(self):
        self.book_window = BookManagerApp()
        self.book_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
