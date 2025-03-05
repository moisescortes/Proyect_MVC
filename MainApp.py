import sys
from PyQt5 import QtWidgets
from dbConnection.FirebaseConnection import FirebaseConnection
from controllers.MainWindowController import MainWindowController

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Conectar a Firebase
    firebase_connection = FirebaseConnection()
    database = firebase_connection.db

    if database is None:
        print("❌ No se pudo conectar a Firebase. Saliendo...")
        sys.exit(1)

    # Crear la ventana principal
    main_window = MainWindowController(database)
    main_window.show_view()

    sys.exit(app.exec_())