from PyQt5 import QtWidgets
from view.ui_mainwindow import Ui_MainWindow  # Importa la UI

class MainWindowView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_connections()

    def setup_connections(self):
        """Conecta señales (botones) a slots (métodos) en el controlador."""
        self.ui.btn_books.clicked.connect(self.open_book_manager)
        self.ui.btn_laptops.clicked.connect(self.open_laptop_manager)
        self.ui.btn_users.clicked.connect(self.open_user_manager)
        self.ui.btn_loans.clicked.connect(self.open_loan_manager)
        self.ui.btn_exit.clicked.connect(self.close)  # Cierra la ventana

    # --- Señales para el controlador ---
    def open_book_manager(self):
        pass  # Se conecta al controlador

    def open_laptop_manager(self):
        pass  # Se conecta al controlador
    
    def open_user_manager(self):
        pass  # Se conecta al controlador
    
    def open_loan_manager(self):
        pass  # Se conecta al controlador