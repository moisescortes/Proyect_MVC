from Proyect_MVC.model.Objects import User

class Admin(User):
    def __init__(self, user_id, name):
        """
        Constructor para la clase Admin.

        :param user_id: Identificador único del administrador.
        :param name: Nombre del administrador.
        """
        super().__init__(user_id, name, "admin")  # Llama al constructor de la clase base

    # Método especial para representación en string
    def __str__(self):
        return f"Admin(ID: {self._user_id}, Name: {self._name})"