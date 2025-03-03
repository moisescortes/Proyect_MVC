from model.DAO.LoanDAO import LoanDAO
from model.Objects.Loan import Loan

class LoanController:
    def __init__(self, database):
        """
        Constructor para la clase LoanController.

        :param database: Objeto de conexión a la base de datos (Firebase).
        """
        self._loan_dao = LoanDAO(database)  # Crear una instancia de LoanDAO

    def solicitar_prestamo(self, loan_id, user_id, item_id, item_type, start_date, due_date):
        """
        Registra un nuevo préstamo en la base de datos.

        :param loan_id: Identificador único del préstamo.
        :param user_id: ID del usuario que solicita el préstamo.
        :param item_id: ID del libro o laptop prestado.
        :param item_type: Tipo de objeto ("book" o "laptop").
        :param start_date: Fecha de inicio del préstamo.
        :param due_date: Fecha de vencimiento del préstamo.
        :return: True si se registró correctamente, False en caso contrario.
        """
        prestamo = Loan(loan_id=loan_id, user_id=user_id, item_id=item_id, item_type=item_type, start_date=start_date, due_date=due_date)
        return self._loan_dao.add_loan(prestamo)

    def devolver_prestamo(self, loan_id):
        """
        Registra la devolución de un préstamo.

        :param loan_id: Identificador único del préstamo.
        :return: True si se actualizó correctamente, False en caso contrario.
        """
        return self._loan_dao.close_loan(loan_id)

    def obtener_prestamos_por_usuario(self, user_id):
        """
        Obtiene todos los préstamos de un usuario.

        :param user_id: Identificador único del usuario.
        :return: Lista de objetos Loan asociados al usuario.
        """
        return self._loan_dao.get_loans_by_user(user_id)

    def obtener_prestamos_por_vencer(self):
        """
        Obtiene todos los préstamos próximos a vencer.

        :return: Lista de préstamos que están por vencer.
        """
        return self._loan_dao.get_due_loans()

    def obtener_todos_los_prestamos(self):
        """
        Obtiene todos los préstamos registrados en la base de datos.

        :return: Lista de objetos Loan.
        """
        return self._loan_dao.get_all_loans()
