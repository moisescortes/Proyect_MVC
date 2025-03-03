from datetime import datetime

class Loan:
    def __init__(self, loan_id, user_id, book_id, start_date, end_date, status="active"):
        """
        Constructor para la clase Loan.

        :param loan_id: Identificador único del préstamo.
        :param user_id: Identificador del usuario que realiza el préstamo.
        :param book_id: Identificador del libro prestado.
        :param start_date: Fecha de inicio del préstamo (en formato 'YYYY-MM-DD').
        :param end_date: Fecha de vencimiento del préstamo (en formato 'YYYY-MM-DD').
        :param status: Estado del préstamo ("active" o "expired"), por defecto es "active".
        """
        self._loan_id = loan_id
        self._user_id = user_id
        self._book_id = book_id
        self._start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self._end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self._status = status

    # Getters
    def get_loan_id(self):
        return self._loan_id

    def get_user_id(self):
        return self._user_id

    def get_book_id(self):
        return self._book_id

    def get_start_date(self):
        return self._start_date

    def get_end_date(self):
        return self._end_date

    def get_status(self):
        return self._status

    # Setters
    def set_loan_id(self, loan_id):
        self._loan_id = loan_id

    def set_user_id(self, user_id):
        self._user_id = user_id

    def set_book_id(self, book_id):
        self._book_id = book_id

    def set_start_date(self, start_date):
        self._start_date = datetime.strptime(start_date, "%Y-%m-%d")

    def set_end_date(self, end_date):
        self._end_date = datetime.strptime(end_date, "%Y-%m-%d")

    def set_status(self, status):
        if status in ["active", "expired"]:
            self._status = status
        else:
            raise ValueError("Invalid status. Use 'active' or 'expired'.")

    # Método para verificar si el préstamo está vencido
    def is_expired(self):
        """
        Verifica si el préstamo está vencido comparando la fecha actual con la fecha de vencimiento.
        """
        return datetime.now() > self._end_date

    # Método para representar el objeto en formato JSON para Firebase
    def to_dict(self):
        """
        Convierte el objeto Loan a un diccionario JSON para almacenar en Firebase.
        """
        return {
            "loan_id": self._loan_id,
            "user_id": self._user_id,
            "book_id": self._book_id,
            "start_date": self._start_date.strftime("%Y-%m-%d"),
            "end_date": self._end_date.strftime("%Y-%m-%d"),
            "status": self._status
        }

    # Método especial para representación en string
    def __str__(self):
        return (f"Loan(ID: {self._loan_id}, User ID: {self._user_id}, Book ID: {self._book_id}, "
                f"Start Date: {self._start_date.strftime('%Y-%m-%d')}, End Date: {self._end_date.strftime('%Y-%m-%d')}, "
                f"Status: {self._status})")