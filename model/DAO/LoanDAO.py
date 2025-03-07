from model.Objects.Loan import Loan
from google.cloud.firestore_v1.base_query import FieldFilter, And
import random
import string

class LoanDAO:
    def __init__(self, database):
        self._database = database
        self._collection = "loans"

    def _generate_loan_id(self):
        """Genera un ID de préstamo único (alfanumérico de 6 caracteres)."""
        while True:
            loan_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not self.loan_exists(loan_id): #Verificamos que no exista.
                return loan_id

    def loan_exists(self, loan_id):
        """Verifica si un préstamo con el ID dado ya existe."""
        try:
            doc_ref = self._database.collection(self._collection).document(loan_id)
            return doc_ref.get().exists
        except Exception as e:
            print(f"Error al verificar la existencia del préstamo: {e}")
            return False  # En caso de error, mejor asumir que no existe

    def add_loan(self, loan):
        try:
            loan_data = loan.to_dict()
            self._database.collection(self._collection).document(loan.get_loan_id()).set(loan_data)
            return True
        except Exception as e:
            print(f"Error al agregar el préstamo: {e}")
            return False

    def get_loan_by_id(self, loan_id):
        try:
            doc_ref = self._database.collection(self._collection).document(loan_id)
            doc = doc_ref.get()
            if doc.exists:
                return Loan(**doc.to_dict())  # Use dictionary unpacking
            return None
        except Exception as e:
            print(f"Error al obtener el préstamo: {e}")
            return None
    
    def update_loan(self, loan):
        """Actualiza un préstamo existente."""
        try:
            doc_ref = self._database.collection(self._collection).document(loan.get_loan_id())
            doc_ref.update(loan.to_dict())  # Actualiza *todos* los campos
            return True
        except Exception as e:
            print(f"Error al actualizar el préstamo: {e}")
            return False

    def delete_loan(self, loan_id):
        try:
            self._database.collection(self._collection).document(loan_id).delete()
            return True
        except Exception as e:
            print(f"Error al eliminar el préstamo: {e}")
            return False

    def get_all_loans(self):
        try:
            loans_list = []
            docs = self._database.collection(self._collection).stream()
            for doc in docs:
                loans_list.append(Loan(**doc.to_dict())) # Use dictionary unpacking
            return loans_list
        except Exception as e:
            print(f"Error al obtener todos los préstamos: {e}")
            return []
    
    def search_loans(self, loan_id):
        """Busca un préstamo por su ID.  Devuelve una lista con el préstamo (o una lista vacía si no se encuentra)."""
        try:
            loan = self.get_loan_by_id(loan_id)  # Usa el método existente!
            if loan:
                return [loan]  # Devuelve una lista con el préstamo encontrado
            else:
                return []  # Devuelve una lista vacía si no se encuentra
        except Exception as e:
            print(f"Error al buscar préstamo por ID: {e}")
            return []
    