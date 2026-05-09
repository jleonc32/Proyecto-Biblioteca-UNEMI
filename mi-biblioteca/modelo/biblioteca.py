from modelo.libro import Libro
from modelo.estudiante import Estudiante
from modelo.profesor import Profesor
from modelo.prestamo import Prestamo
from typing import Union
from datetime import datetime


class Biblioteca:
    """gestiona libros, estudiantes y orestamos"""
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._libros = []       
        self._estudiantes = []       
        self._profesores = []       
        self._prestamos = []
        
    def registrar_libro(self, libro: Libro)-> None:
        """agregar un libro al catálago de la biblioteca"""
        self._libros.append(libro)
        print(f" ✓ Libro registrado: {libro.titulo}")
        
    def registrar_estudiante(self, estudiante: Estudiante) ->None:
        """registrar estudiante a la biblioteca"""
        self._estudiantes.append(estudiante)
        print(f" ✓ Estudiante registrado: {estudiante.nombre} {estudiante.apellido}")
        
    def registrar_profesor(self, profesor:Profesor):
        """registra profesores en lam biblioteca"""
        self._profesores.append(profesor)
        print(f" ✓ Profesor registrado: {profesor.nombre} {profesor.apellido} {profesor.departamento}")
        
    def _buscar_libro(self, isbn: str) ->Libro:
        """busca un libro por isbn. Retorna none si no existe"""
        for libro in self._libros:
            if libro.isbn == isbn:
                return libro
        return None
    
    def _buscar_usuario(self, cedula: str) ->Union[Estudiante, Profesor]:
        """busca un usuario por ceula. returna none si no existe"""
        for estudiante in self._estudiantes:
            if estudiante.cedula == cedula:
                return estudiante
            
        for profesor in self._profesores:
            if profesor.cedula == cedula:
                return profesor
            
        return None
    
    def prestar_libro(self, isbn: str, cedula: str, fecha_prestamo: str, fecha_devolucion: str) -> str:
        """Registra un préstamo si el libro esta disponible"""
        libro = self._buscar_libro(isbn)
        if libro is None:
            return f"  ✗ ERROR: No se encontró el libro con ISBN{isbn}"
        
        usuario = self._buscar_usuario(cedula)
        if usuario is None:
            return f"  ✗ ERROR. No se encontro el usuario con cédula {cedula}"
        
        if not libro.disponible:
            return f" ✗ ERROR. El libro '{libro.titulo}' no está disponible"
        
        
        libro.prestar()
        prestamo = Prestamo(libro, usuario, fecha_prestamo, fecha_devolucion)
        self._prestamos.append(prestamo)
        return f" ✓ Préstamo registrado: '{libro.titulo}' → {usuario.nombre}"

    def devolver_libro(self, isbn: str, cedula: str) ->str:
        """Registrar la devolucion de un libro."""
        for prestamo in self._prestamos:
            if(prestamo.libro.isbn == isbn and prestamo.usuario.cedula == cedula and prestamo.activo):
                """logica de multas"""
                mensaje_multa =""
                #convertir fechas
                fecha_pactada = datetime.strptime(prestamo.fecha_devolucion, "%Y-%m-%d")
                fecha_actual = datetime.now()
                
                #si la fecha es mayor a la de entrega hay multa
                if fecha_actual > fecha_pactada:
                    dias_retraso = (fecha_actual - fecha_pactada). days
                    if dias_retraso > 0:
                        total_multa = dias_retraso * 0.50
                        mensaje_multa = f"\n Recargo Por Retraso: {dias_retraso} dias. Multa: {total_multa}$"
                prestamo.registrar_devolucion()        
                return f"  ✓ Devolución registrada: '{prestamo.libro.titulo}', {mensaje_multa}"
        return " ✗ Error: No se encontró un préstamo activo con esos datos"   
    
    def consultar_prestamos_activos(self, cedula: str) -> list:
        """retorna los préstamos activos de un estudiante"""
        activos = []
        for prestamo in self._prestamos:
            if prestamo.usuario.cedula == cedula and prestamo.activo:
                activos.append(prestamo)
        return activos 
    
    def mostrar_catalogo(self):
        """Muestra los libros registrados ordenados alfabéticamente por título (Reto 2)"""
        if not self._libros:
            print("\n ℹ️ El catálogo está vacío.")
            return

        # Ordenamos la lista de libros usando el atributo título como clave
        # .lower() asegura que el orden sea correcto sin importar mayúsculas
        libros_ordenados = sorted(self._libros, key=lambda libro: libro.titulo.lower())

        print("\n" + "="*75)
        print(f"║{'CATÁLOGO DE LIBROS ORDENADO (UNEMI)':^73}║")
        print("="*75)
        print(f"║ {'ISBN':<20} │ {'TÍTULO':<30} │ {'ESTADO':<15} ║")
        print("╟" + "─"*22 + "┼" + "─"*32 + "┼" + "─"*17 + "╢")

        for libro in libros_ordenados:
            estado = "✅ Disponible" if libro.disponible else "❌ Prestado"
            print(f"║ {libro.isbn:<20} │ {libro.titulo:<30} │ {estado:<15} ║")
        
        print("╚" + "═"*73 + "╝")
    
    def __str__(self) -> str:
        return(f"Biblioteca '{self._nombre}' | "
               f"Libros: {len(self._libros)} | "
               f"Estudiantes: {len(self._estudiantes)} | "
               f"Profesores: {len(self._profesores)} | "
               f"Prestamos: {len(self._prestamos)}")
        
        
        