from db import conectar, insertar_medicamento, obtener_medicamentos
from ui.dashboard import iniciar_app
from db import conectar, insertar_medicamento, obtener_medicamentos


def main():
    print("Iniciando programa...")

    conexion = conectar()
    if conexion:
        print("Todo bien 👍")

    # insertar_muchos_medicamentos()  ❌ YA NO

    print("\nLista de medicamentos:")
    datos = obtener_medicamentos()

    for fila in datos:
        print(fila)

if __name__ == "__main__":
    main()


def main():
    print("Iniciando programa...")

    # Probar conexión
    conexion = conectar()
    if conexion:
        print("Todo bien ")

    # Insertar medicamento de prueba
    insertar_medicamento(
        "Ibuprofeno",
        30,
        8.5,
        12.0,
        "2025-10-20"
    
    )

    # Obtener y mostrar medicamentos
    print("\nLista de medicamentos:")
    datos = obtener_medicamentos()

    for fila in datos:
        print(fila)

    #  NUEVO: iniciar interfaz
    print("Abriendo interfaz...")
    iniciar_app()


if __name__ == "__main__":
    main()