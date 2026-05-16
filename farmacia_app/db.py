import mysql.connector

print("Cargando db.py...")

def buscar_por_sintoma(sintoma):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM medicamentos WHERE sintoma LIKE %s",
            ("%" + sintoma + "%",)
        )

        datos = cursor.fetchall()
        conexion.close()

        return datos

    except Exception as e:
        print("Error:", e)


def buscar_por_sintoma(sintoma):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM medicamentos WHERE sintoma LIKE %s",
            ("%" + sintoma + "%",)
        )

        datos = cursor.fetchall()
        conexion.close()

        return datos

    except Exception as e:
        print("Error:", e)
        return[]

def insertar_medicamento(nombre, stock, compra, venta, fecha, sintoma):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO medicamentos 
            (nombre, stock, precio_compra, precio_venta, fecha_caducidad, sintoma)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, stock, compra, venta, fecha, sintoma))

        conexion.commit()
        conexion.close()

    except Exception as e:
        print("Error:", e)

def insertar_muchos_medicamentos():
    medicamentos = [
        "Paracetamol","Ibuprofeno","Ácido acetilsalicílico","Naproxeno","Diclofenaco",
        "Loratadina","Cetirizina","Clorfenamina","Ambroxol","Dextrometorfano","Fenilefrina",
        "Amoxicilina","Ampicilina","Azitromicina","Ciprofloxacino","Metronidazol",
        "Ketorolaco","Tramadol",
        "Losartán","Enalapril","Amlodipino","Atenolol",
        "Metformina","Glibenclamida",
        "Diazepam","Clonazepam",
        "Fluconazol","Aciclovir","Nitrofurantoína",
        "Omeprazol","Ranitidina","Loperamida","Hidróxido de aluminio",
        "Sales de rehidratación oral",
        "Insulina","Salbutamol","Budesonida","Prednisona","Hidrocortisona",
        "Agua oxigenada","Alcohol","Gel antibacterial","Suero fisiológico",
        "Vitamina C","Complejo B"
    ]

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        for med in medicamentos:
            cursor.execute("""
                INSERT INTO medicamentos (nombre, stock, precio_compra, precio_venta, fecha_caducidad)
                VALUES (%s, %s, %s, %s, %s)
            """, (med, 20, 10, 15, "2026-12-31"))

        conexion.commit()
        conexion.close()

        print("Medicamentos insertados correctamente")

    except Exception as e:
        print("Error:", e)

def conectar():
    try:
        print("Intentando conectar...")

        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # cambia si es necesario
            database="farmacia"
        )

        print("Conexión exitosa a MariaDB")
        return conexion

    except Exception as e:
        print("ERROR REAL:", e)


# ===============================
# INSERTAR MEDICAMENTO
# ===============================

def insertar_medicamento(nombre, stock, precio_compra, precio_venta, fecha):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO medicamentos (nombre, stock, precio_compra, precio_venta, fecha_caducidad)
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (nombre, stock, precio_compra, precio_venta, fecha)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Medicamento insertado correctamente")

        conexion.close()

    except Exception as e:
        print("Error al insertar:", e)


# ===============================
# OBTENER MEDICAMENTOS
# ===============================

def obtener_medicamentos():
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM medicamentos")
        datos = cursor.fetchall()

        conexion.close()

        return datos

    except Exception as e:
        print("Error al obtener datos:", e)

  # ===============================
# BUSCAR MEDICAMENTOS
# ===============================

def buscar_medicamentos(texto):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = "SELECT * FROM medicamentos WHERE nombre LIKE %s"
        cursor.execute(sql, ("%" + texto + "%",))

        datos = cursor.fetchall()
        conexion.close()

        return datos

    except Exception as e:
        print("Error al buscar:", e)
        
 # ===============================
# ELIMINAR MEDICAMENTO
# ===============================
def eliminar_medicamento(id):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM medicamentos WHERE id = %s", (id,))
        conexion.commit()

        print("Medicamento eliminado")

        conexion.close()

    except Exception as e:
        print("Error al eliminar:", e)


# ===============================
# VENDER MEDICAMENTO
# ===============================
def vender_medicamento(id, cantidad):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT stock FROM medicamentos WHERE id = %s", (id,))
        resultado = cursor.fetchone()

        if resultado:
            stock_actual = resultado[0]

            if stock_actual >= cantidad:
                nuevo_stock = stock_actual - cantidad

                cursor.execute(
                    "UPDATE medicamentos SET stock = %s WHERE id = %s",
                    (nuevo_stock, id)
                )
                conexion.commit()

                print("Venta realizada")
            else:
                print("Stock insuficiente")

        conexion.close()

    except Exception as e:
        print("Error en venta:", e)
# ===============================
# MEDICAMENTOS POR CADUCAR
# ===============================
def obtener_por_caducar(dias=30):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT * FROM medicamentos
            WHERE fecha_caducidad <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
        """, (dias,))

        datos = cursor.fetchall()
        conexion.close()

        return datos

    except Exception as e:
        print("Error caducidad:", e)

# ===============================
# VENTAS AGRUPADAS POR MEDICAMENTO
# ===============================
def ventas_por_medicamento():
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT m.nombre, SUM(v.cantidad)
            FROM ventas v
            JOIN medicamentos m ON v.medicamento_id = m.id
            GROUP BY m.nombre
        """)

        datos = cursor.fetchall()
        conexion.close()

        return datos

    except Exception as e:
        print("Error en gráfica:", e)
        return []
        
    
# ===============================
# STOCK BAJO
# ===============================
def obtener_stock_bajo(limite=10):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM medicamentos WHERE stock <= %s",
            (limite,)
        )

        datos = cursor.fetchall()
        conexion.close()

        return datos

    except Exception as e:
        print("Error stock bajo:", e)
        return []
      