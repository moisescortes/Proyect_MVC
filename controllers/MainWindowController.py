from PyQt5 import QtWidgets
from view.ui_mainwindow import Ui_MainWindow
from controllers.BookController import BookController
from controllers.LaptopController import LaptopController
from controllers.UserController import UserController
from controllers.LoanController import LoanController

class MainWindowController(QtWidgets.QMainWindow):
    def __init__(self, database):
        super().__init__()
        self.database = database  # Referencia a la base de datos
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_signals()
        # Inicializa los controladores como None
        self.book_controller = None
        self.laptop_controller = None
        self.user_controller = None
        self.loan_controller = None

    def connect_signals(self):
        """Conecta las señales de la vista a los slots del controlador."""
        self.ui.btn_books.clicked.connect(self.show_book_manager)
        self.ui.btn_laptops.clicked.connect(self.show_laptop_manager)
        self.ui.btn_users.clicked.connect(self.show_user_manager)
        self.ui.btn_loans.clicked.connect(self.show_loan_manager)
        self.ui.btn_exit.clicked.connect(self.close_application)  # Salir

    def show_view(self):
        """Muestra la ventana principal."""
        self.show()

    def show_book_manager(self):
        """Muestra la ventana de gestión de libros."""
        show_book_manager = BookController(self.database)
        show_book_manager.exec_()

    def show_laptop_manager(self):
        """Muestra la ventana de gestión de laptops (implementar)."""
        show_book_manager = LaptopController(self.database)
        show_book_manager.exec_()
        
    def show_user_manager(self):
        """Muestra la ventana de gestión de usuarios (implementar)."""
        show_book_manager = UserController(self.database)
        show_book_manager.exec_()

    def show_loan_manager(self):
        """Muestra la ventana de gestión de préstamos (implementar)."""
        show_book_manager = LoanController(self.database)
        show_book_manager.exec_()

    def close_application(self):
        """Cierra la aplicación."""
        self.close()