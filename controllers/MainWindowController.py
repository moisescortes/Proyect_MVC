from view.mainwindow import MainWindowView
from controllers.BookController import BookController
#from controllers.LaptopController import LaptopController
from controllers.UserController import UserController
#from controllers.LoanController import LoanController


class MainWindowController:
    def __init__(self, database):
        self.database = database  # Referencia a la base de datos
        self.view = MainWindowView()
        self.connect_signals()
        # Inicializa los controladores como None
        self.book_controller = None
        self.laptop_controller = None
        self.user_controller = None
        self.loan_controller = None

    def connect_signals(self):
        """Conecta las señales de la vista a los slots del controlador."""
        self.view.ui.btn_books.clicked.connect(self.show_book_manager)
        self.view.ui.btn_laptops.clicked.connect(self.show_laptop_manager)
        self.view.ui.btn_users.clicked.connect(self.show_user_manager)
        self.view.ui.btn_loans.clicked.connect(self.show_loan_manager)
        self.view.ui.btn_exit.clicked.connect(self.close_application)  # Salir

    def show_view(self):
        """Muestra la ventana principal."""
        self.view.show()

    def show_book_manager(self):
        """Muestra la ventana de gestión de libros."""
        if self.book_controller is None:  # Crea el controlador solo si no existe
            self.book_controller = BookController(self.database)  # Pasa la conexión
        self.book_controller.show_view()

    def show_laptop_manager(self):
        """Muestra la ventana de gestión de laptops (implementar)."""
        # if self.laptop_controller is None:
        #     self.laptop_controller = LaptopController(self.database)
        # self.laptop_controller.show_view()
        pass
        
    def show_user_manager(self):
        """Muestra la ventana de gestión de usuarios (implementar)."""
        if self.user_controller is None:
            self.user_controller = UserController(self.database)
        self.user_controller.show_view()

    def show_loan_manager(self):
        """Muestra la ventana de gestión de préstamos (implementar)."""
        # if self.loan_controller is None:
        #     self.loan_controller = LoanController(self.database)
        # self.loan_controller.show_view()
        pass

    def close_application(self):
        """Cierra la aplicación."""
        self.view.close()