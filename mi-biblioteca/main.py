# main.py
from faker import Faker
from modelo.libro import Libro
from modelo.estudiante import Estudiante
from modelo.profesor import Profesor
from modelo.biblioteca import Biblioteca



def main():
    fake = Faker('es_ES')
    # --- Crear la biblioteca ---
    print("=" * 60)
    print("  SISTEMA DE GESTION DE BIBLIOTECA UNEMI")
    print("=" * 60)

    biblioteca = Biblioteca("Biblioteca Central UNEMI")
    print(f"\n{biblioteca}\n")

    # --- Registrar libros (RF-01) ---
    print("--- Registrando libros ---")
    libro1 = Libro("978-0-13-468599-1", "El Principito", "Antoine de Saint-Exupéry")
    libro2 = Libro("978-0-06-112008-4", "Cien Años de Soledad", "Gabriel García Márquez")
    libro3 = Libro("978-84-376-0494-7", "Don Quijote de la Mancha", "Miguel de Cervantes")
    libro4 = Libro("978-84-376-0495-5", "Libro de Prueba", "Autor Test")
    libro5 = Libro("978-84-376-0496-6", "El leon, Labruja y El armario", "lewis")

    biblioteca.registrar_libro(libro1)
    biblioteca.registrar_libro(libro2)
    biblioteca.registrar_libro(libro3)
    biblioteca.registrar_libro(libro4)
    biblioteca.registrar_libro(libro5)

    # --- Registrar estudiantes (RF-02) ---
    print("\n--- Registrando estudiantes ---")
    est1 = Estudiante("0926400615", "María", "López", "Ingeniería en Sistemas")
    est2 = Estudiante("0912345678", "Carlos", "Ramírez", "Ingeniería Industrial")

    biblioteca.registrar_estudiante(est1)
    biblioteca.registrar_estudiante(est2)
    
    # --- Registrar Profesor (RF-02) ---
    print("\n--- Registrando profesor ---")
    prof1 = Profesor("0926405555", "Ronaldinho", "Gaucho", "ciencias e ingenieria")
    prof2 = Profesor("0912346666", "Leonel", "Messi", "salud")
    prof3 = Profesor("0912347777", "Neymar", "Junior", "Fisica")
    
    biblioteca.registrar_profesor(prof1)
    biblioteca.registrar_profesor(prof2)
    biblioteca.registrar_profesor(prof3)
    
    for _ in range(5):
        biblioteca.registrar_libro(Libro(fake.isbn13(), fake.catch_phrase().title(), fake.name()))
        
    # --- Registrar estudiantes aleatorios con Faker ---
    print("\n--- Registrando estudiantes con Faker ---")
    for _ in range(8):  # Generamos 5 estudiantes
        cedula_fake = str(fake.random_number(digits=10, fix_len=True))
        nombre_fake = fake.first_name()
        apellido_fake = fake.last_name()
        carrera_fake = fake.job() # O puedes poner "Ingeniería" fijo
        
        nuevo_est = Estudiante(cedula_fake, nombre_fake, apellido_fake, carrera_fake)
        biblioteca.registrar_estudiante(nuevo_est)
        
    print("\n--- Registrando profesores con Faker ---")
    facultades = ["Ciencias e Ingeniería", "Salud", "Educación", "Sociales"]
    for _ in range(7):  # Generamos 3 profesores
        cedula_fake = str(fake.random_number(digits=10, fix_len=True))
        nombre_fake = fake.first_name()
        apellido_fake = fake.last_name()
        depto_fake = fake.random_element(elements=facultades)
        
        nuevo_prof = Profesor(cedula_fake, nombre_fake, apellido_fake, depto_fake)
        biblioteca.registrar_profesor(nuevo_prof)

    # --- Estado actual ---
    print(f"\n{biblioteca}\n")

    # --- Realizar préstamos (RF-03 y RF-04) ---
    print("--- Realizando préstamos ---")
    resultado = biblioteca.prestar_libro(
        "978-0-13-468599-1", "0926400615", "2026-04-15", "2026-04-29"
    )
    print(resultado)
    
    resultado = biblioteca.prestar_libro(
        "978-84-376-0496-6", "0926405555", "2026-04-15", "2026-04-20"
    )
    print(resultado)


    resultado = biblioteca.prestar_libro(
        "978-0-06-112008-4", "0926400615", "2026-04-15", "2026-05-01"
    )
    print(resultado)

    resultado = biblioteca.prestar_libro(
        "978-84-376-0494-7", "0912345678", "2026-04-15", "2026-04-22"
    )
    print(resultado)
    
    resultado = biblioteca.prestar_libro(
        "978-0-06-112008-4", "0926405555", "2026-04-15", "2026-05-01"
    )
    print(resultado)

    # --- Intentar prestar un libro ya prestado (RF-04: validación) ---
    print("\n--- Intentando prestar libro ya prestado ---")
    resultado = biblioteca.prestar_libro(
        "978-0-13-468599-1", "0912345678", "2026-04-16", "2026-04-30"
    )
    print(resultado)
    # --- Consultar multas (RF-06) ---
    print("\n" + "="*60)
    print("  PRUEBA DE MULTAS (RETRASO)")
    print("="*60)
    
    print("Registrando préstamo atrasado para María...")
    resultado_p = biblioteca.prestar_libro(
        "978-84-376-0495-5", "0926400615", "2026-04-01", "2026-04-20"
    )
    print(resultado_p)

    # --- Consultar préstamos activos (RF-06) ---
    print("\n--- Préstamos activos de María López ---")
    prestamos_maria = biblioteca.consultar_prestamos_activos("0926400615")
    for prestamo in prestamos_maria:
        print(f"  → {prestamo}")

    # --- Devolver un libro (RF-05) ---
    print("\n--- Devolviendo un libro ---")
    resultado = biblioteca.devolver_libro("978-0-13-468599-1", "0926400615")
    print(resultado)
    
    print("\n--- Devolviendo un libro ---")
    resultado = biblioteca.devolver_libro("978-84-376-0496-6", "0926405555")
    print(resultado)
    
    print("\n---Devolviendo el libro hoy ---")
    # El sistema comparará la fecha actual (29 de abril) vs la pactada (20 de abril)
    res_d = biblioteca.devolver_libro("978-84-376-0495-5", "0926400615")
    print(res_d)

    # --- Verificar que el libro está disponible nuevamente ---
    print(f"\n--- Estado del libro devuelto ---")
    print(f"  {libro1}")

    # --- Consultar préstamos activos después de devolución ---
    print("\n--- Préstamos activos de María López (después de devolución) ---")
    prestamos_maria = biblioteca.consultar_prestamos_activos("0926400615")
    if prestamos_maria:
        for prestamo in prestamos_maria:
            print(f"  → {prestamo}")
    else:
        print("  (Sin préstamos activos)")

    # --- Ahora el libro puede prestarse de nuevo ---
    print("\n--- Prestando el libro devuelto a otro estudiante ---")
    resultado = biblioteca.prestar_libro(
        "978-0-13-468599-1", "0912345678", "2026-04-16", "2026-04-30"
    )
    print(resultado)
        
    # En tu archivo main.py
    print("\n--- Generando Catálogo Ordenado ---")
    biblioteca.mostrar_catalogo()

    # --- Estado final ---
    print(f"\n{'=' * 60}")
    print(f"  {biblioteca}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()