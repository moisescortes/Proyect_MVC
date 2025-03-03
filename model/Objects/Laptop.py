class Laptop:
    def __init__(self, laptop_id, brand, model, status="available"):
        """
        Constructor para la clase Laptop.

        :param laptop_id: Identificador único de la laptop.
        :param brand: Marca de la laptop.
        :param model: Modelo de la laptop.
        :param status: Estado de la laptop ("available" o "borrowed"), por defecto es "available".
        """
        self._laptop_id = laptop_id
        self._brand = brand
        self._model = model
        self._status = status

    # Getters
    def get_laptop_id(self):
        return self._laptop_id

    def get_brand(self):
        return self._brand

    def get_model(self):
        return self._model

    def get_status(self):
        return self._status

    # Setters
    def set_laptop_id(self, laptop_id):
        self._laptop_id = laptop_id

    def set_brand(self, brand):
        self._brand = brand

    def set_model(self, model):
        self._model = model

    def set_status(self, status):
        if status in ["available", "borrowed"]:
            self._status = status
        else:
            raise ValueError("Invalid status. Use 'available' or 'borrowed'.")

    # Método para representar el objeto en formato JSON para Firebase
    def to_dict(self):
        """
        Convierte el objeto Laptop a un diccionario JSON para almacenar en Firebase.
        """
        return {
            "laptop_id": self._laptop_id,
            "brand": self._brand,
            "model": self._model,
            "status": self._status
        }

    # Método especial para representación en string
    def __str__(self):
        return f"Laptop(ID: {self._laptop_id}, Brand: {self._brand}, Model: {self._model}, Status: {self._status})"