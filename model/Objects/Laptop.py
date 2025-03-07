class Laptop:
    def __init__(self, laptop_id, brand, model, serial_number, status):
        self._laptop_id = laptop_id
        self._brand = brand
        self._model = model
        self._serial_number = serial_number
        self._status = status

    def get_laptop_id(self):
        return self._laptop_id

    def get_brand(self):
        return self._brand

    def get_model(self):
        return self._model
    
    def get_serial_number(self):
        return self._serial_number

    def get_status(self):
        return self._status
    
    def set_status(self, status):
        self._status = status

    def to_dict(self):
        return {
            "laptop_id": self._laptop_id,
            "brand": self._brand,
            "model": self._model,
            "serial_number": self._serial_number,
            "status": self._status,
        }