from Proyect_MVC.model.Objects import User

class Student(User):
    def __init__(self, user_id, name, career):
        """
        Constructor para la clase Student.

        :param user_id: Identificador único del estudiante.
        :param name: Nombre del estudiante.
        :param career: Carrera que estudia el estudiante.
        """
        super().__init__(user_id, name, "student")  # Llama al constructor de la clase base
        self._career = career

    # Getter y Setter para career
    def get_career(self):
        return self._career

    def set_career(self, career):
        self._career = career

    # Método para representar el objeto en formato JSON para Firebase
    def to_dict(self):
        """
        Convierte el objeto Student a un diccionario JSON para almacenar en Firebase.
        """
        user_dict = super().to_dict()  # Obtiene el diccionario de la clase base
        user_dict["career"] = self._career  # Agrega el atributo específico de Student
        return user_dict

    # Método especial para representación en string
    def __str__(self):
        return f"Student(ID: {self._user_id}, Name: {self._name}, Career: {self._career})"