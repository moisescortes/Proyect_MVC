import sys
from PyQt5.QtWidgets import QApplication
from controllers.MainWindowController import MainWindowController  # Controlador de MainWindow
from dbConnection.FirebaseConnection import FirebaseConnection

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # --- Conexión a Firebase ---
    try:
        firebase_connection = FirebaseConnection()
        database = firebase_connection.db
        print("Conexión a Firebase exitosa.")
    except Exception as e:
        print(f"Error al conectar a Firebase: {e}")
        sys.exit(1)

    # Instancia el controlador de la ventana principal y pasa la conexión
    main_window_controller = MainWindowController(database)
    main_window_controller.show_view() # Mostrar MainWindow

    sys.exit(app.exec_())