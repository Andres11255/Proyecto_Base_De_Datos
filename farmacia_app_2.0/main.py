from db import conectar, obtener_medicamentos
from ui.inventario import abrir_inventario

def main():
    print("Iniciando Sistema de Farmacia PRO...")

    # Probar conexión a la base de datos local JSON
    conexion = conectar()
    if conexion:
        print("Todo bien - Base de datos local (JSON) cargada correctamente")

    # Mostrar medicamentos en la consola como estaba antes
    print("\nLista de medicamentos (Consola):")
    try:
        datos = obtener_medicamentos()
        for fila in datos:
            print(fila)
    except Exception as e:
        print("Error al obtener la lista de medicamentos:", e)

    # Iniciar la interfaz gráfica principal (inventario)
    print("Abriendo interfaz principal...")
    abrir_inventario()

if __name__ == "__main__":
    main()