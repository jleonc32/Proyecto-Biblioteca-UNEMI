class Persona:
    
    def __init__(self, cedula = str, nombre = str, apellido = str):
        self._cedula = cedula
        self._nombre = nombre
        self._apellido = apellido
        
    @property
    def cedula(self):
        return self._cedula
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def apellido(self):
        return self._apellido
    
    def __str__(self):
        return f'{self._cedula}: {self._nombre} {self._apellido}'
     
        