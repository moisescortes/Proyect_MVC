from datetime import datetime
from model.Objects.Loan import Loan 

class LoanDAO:
    def __init__(self, database):
        """
        Constructor para la clase LoanDAO.

        :param database: Objeto de conexión a la base de datos (o Firebase).
        """
        self._database = database
        self._collection = "loans"  # Nombre de la colección/tabla de préstamos en la base de datos

    def add_loan(self, loan):
        """
        Agrega un nuevo préstamo a la base de datos.

        :param loan: Objeto de tipo Loan.
        :return: True si se agregó correctamente, False en caso contrario.
        """
        try:
            # Convertir el objeto Loan a un diccionario
            loan_data = loan.to_dict()
            # Agregar el préstamo a la colección "loans"
            self._database.child(self._collection).push(loan_data)
            return True
        except Exception as e:
            print(f"Error al agregar el préstamo: {e}")
            return False

    def get_loan_by_id(self, loan_id):
        """
        Obtiene un préstamo por su ID.

        :param loan_id: Identificador único del préstamo.
        :return: Objeto de tipo Loan si se encuentra, None en caso contrario.
        """
        try:
            # Buscar el préstamo por su ID en la colección "loans"
            loans = self._database.child(self._collection).get()
            if loans:
                for key, value in loans.items():
                    if value["loan_id"] == loan_id:
                        return Loan(
                            loan_id=value["loan_id"],
                            user_id=value["user_id"],
                            book_id=value["book_id"],
                            start_date=value["start_date"],
                            end_date=value["end_date"],
                            status=value["status"]
                        )
            return None
        except Exception as e:
            print(f"Error al obtener el préstamo: {e}")
            return None

    def update_loan(self, loan):
        """
        Actualiza un préstamo en la base de datos.

        :param loan: Objeto de tipo Loan con los datos actualizados.
        :return: True si se actualizó correctamente, False en caso contrario.
        """
        try:
            # Convertir el objeto Loan a un diccionario
            loan_data = loan.to_dict()
            # Buscar el préstamo por su ID en la colección "loans"
            loans = self._database.child(self._collection).get()
            if loans:
                for key, value in loans.items():
                    if value["loan_id"] == loan.get_loan_id():
                        # Actualizar el préstamo en la base de datos
                        self._database.child(self._collection).child(key).update(loan_data)
                        return True
            return False
        except Exception as e:
            print(f"Error al actualizar el préstamo: {e}")
            return False

    def delete_loan(self, loan_id):
        """
        Elimina un préstamo de la base de datos.

        :param loan_id: Identificador único del préstamo.
        :return: True si se eliminó correctamente, False en caso contrario.
        """
        try:
            # Buscar el préstamo por su ID en la colección "loans"
            loans = self._database.child(self._collection).get()
            if loans:
                for key, value in loans.items():
                    if value["loan_id"] == loan_id:
                        # Eliminar el préstamo de la base de datos
                        self._database.child(self._collection).child(key).remove()
                        return True
            return False
        except Exception as e:
            print(f"Error al eliminar el préstamo: {e}")
            return False

    def get_all_loans(self):
        """
        Obtiene todos los préstamos de la base de datos.

        :return: Lista de objetos de tipo Loan.
        """
        try:
            loans_list = []
            # Obtener todos los préstamos de la colección "loans"
            loans = self._database.child(self._collection).get()
            if loans:
                for key, value in loans.items():
                    loan = Loan(
                        loan_id=value["loan_id"],
                        user_id=value["user_id"],
                        book_id=value["book_id"],
                        start_date=value["start_date"],
                        end_date=value["end_date"],
                        status=value["status"]
                    )
                    loans_list.append(loan)
            return loans_list
        except Exception as e:
            print(f"Error al obtener todos los préstamos: {e}")
            return []

    def get_loans_by_user(self, user_id):
        """
        Obtiene todos los préstamos asociados a un usuario.

        :param user_id: Identificador único del usuario.
        :return: Lista de objetos de tipo Loan.
        """
        try:
            loans_list = []
            # Obtener todos los préstamos de la colección "loans"
            loans = self._database.child(self._collection).get()
            if loans:
                for key, value in loans.items():
                    if value["user_id"] == user_id:
                        loan = Loan(
                            loan_id=value["loan_id"],
                            user_id=value["user_id"],
                            book_id=value["book_id"],
                            start_date=value["start_date"],
                            end_date=value["end_date"],
                            status=value["status"]
                        )
                        loans_list.append(loan)
            return loans_list
        except Exception as e:
            print(f"Error al obtener los préstamos del usuario: {e}")
            return []

    def get_active_loans(self):
        """
        Obtiene todos los préstamos activos.

        :return: Lista de objetos de tipo Loan.
        """
        try:
            loans_list = []
            # Obtener todos los préstamos de la colección "loans"
            loans = self._database.child(self._collection).get()
            if loans:
                for key, value in loans.items():
                    if value["status"] == "active":
                        loan = Loan(
                            loan_id=value["loan_id"],
                            user_id=value["user_id"],
                            book_id=value["book_id"],
                            start_date=value["start_date"],
                            end_date=value["end_date"],
                            status=value["status"]
                        )
                        loans_list.append(loan)
            return loans_list
        except Exception as e:
            print(f"Error al obtener los préstamos activos: {e}")
            return []