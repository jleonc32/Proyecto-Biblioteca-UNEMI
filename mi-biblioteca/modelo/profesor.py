from modelo.persona import Persona

class Profesor(Persona):
    def __init__(self, cedula=..., nombre=..., apellido=..., departamento = str):
        super().__init__(cedula, nombre, apellido)
        self._departamento = departamento
        
    @property
    def departamento(self):
        return self._departamento
    
    def __str__(self):
        return f"{super().__str__()} | departamento: {self._departamento}."