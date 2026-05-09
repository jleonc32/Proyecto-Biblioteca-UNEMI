from modelo.libro import Libro
from modelo.persona import Persona

class Prestamo:
    """Representa un prestamo de un libro a un estudiante"""
    def __init__(self, libro: Libro, usuario: Persona, fecha_prestamo: str, fecha_devolucion: str):
        self._libro = libro
        self._usuario = usuario
        self._fecha_prestamo = fecha_prestamo
        self._fecha_devolucion = fecha_devolucion
        self._activo = True
        
    @property
    def libro(self) ->Libro:
        return self._libro
    
    @property
    def usuario(self) ->Persona:
        return self._usuario
    
    @property
    def activo(self) ->bool:
        return self._activo 
    
    @property
    def fecha_devolucion(self):
        return self._fecha_devolucion
    
    
    def registrar_devolucion(self) ->None:
        """marca el prestamo como devuelto y libera el libro"""
        self._activo = False
        self._libro.devolver()
        
    def __str__(self) ->str:
        estado = "ACTIVO" if self._activo else "DEVUELTO"
        return (f"Préstamo [{estado}]: {self.libro.titulo} ->"
                f"{self._usuario.nombre} {self._usuario.apellido} | "
                f"Desde: {self._fecha_prestamo} | "
                f"Hasta: {self._fecha_devolucion}")
        
        