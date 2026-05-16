import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

from db import (
    insertar_medicamento,
    obtener_medicamentos,
    buscar_medicamentos,
    buscar_por_sintoma,
    eliminar_medicamento,
    vender_medicamento,
    obtener_stock_bajo,
    obtener_por_caducar
)

from ui.grafica import abrir_grafica


def abrir_inventario():

    ventana = tk.Toplevel()
    ventana.title("💊 Sistema de Farmacia PRO")
    ventana.geometry("1200x650")
    ventana.configure(bg="#1e1e2f")

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=3)
    ventana.columnconfigure(2, weight=1)
    ventana.rowconfigure(1, weight=1)

    # ===============================
    # ALERTAS
    # ===============================
    alerta = tk.Label(
        ventana,
        text="",
        bg="#1e1e2f",
        fg="yellow",
        font=("Arial", 11, "bold")
    )
    alerta.grid(row=0, column=1, sticky="n")

    def actualizar_alertas():
        bajos = len(obtener_stock_bajo())
        caducar = len(obtener_por_caducar())

        alerta.config(
            text=f"⚠ Stock bajo: {bajos} | Por caducar: {caducar}"
        )

    # ===============================
    # PANEL IZQUIERDO
    # ===============================
    frame_left = tk.Frame(ventana, bg="#1e1e2f")
    frame_left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10)

    def campo(texto):
        tk.Label(frame_left, text=texto, fg="white", bg="#1e1e2f").pack(anchor="w")
        entrada = tk.Entry(frame_left)
        entrada.pack(fill="x", pady=3)
        return entrada

    entry_nombre = campo("Nombre")
    entry_stock = campo("Stock")
    entry_compra = campo("Compra")
    entry_venta = campo("Venta")
    entry_fecha = campo("Caducidad")

    tk.Label(frame_left, text="Síntoma", fg="white", bg="#1e1e2f").pack(anchor="w")
    combo_sintoma = ttk.Combobox(frame_left, values=[
        "Dolor", "Tos", "Alergia", "Estómago", "Gripa", "Fiebre"
    ])
    combo_sintoma.pack(fill="x", pady=3)

    entry_buscar = tk.Entry(frame_left)
    entry_buscar.pack(fill="x", pady=10)

    # ===============================
    # TABLA
    # ===============================
    frame_center = tk.Frame(ventana)
    frame_center.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    columnas = ("ID", "Nombre", "Stock", "Compra", "Venta", "Caducidad")

    tabla = ttk.Treeview(frame_center, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)

    tabla.column("ID", width=50, anchor="center")
    tabla.column("Nombre", width=150)
    tabla.column("Stock", width=70, anchor="center")
    tabla.column("Compra", width=90)
    tabla.column("Venta", width=90)
    tabla.column("Caducidad", width=100)

    tabla.pack(fill="both", expand=True)

    # Colores
    tabla.tag_configure("bajo", background="#ff4d4d")
    tabla.tag_configure("caducar", background="#ffcc00")

    # ===============================
    # PANEL DERECHO (FUTURO)
    # ===============================
    frame_right = tk.Frame(ventana, bg="#2b2b3c")
    frame_right.grid(row=0, column=2, sticky="nsew", padx=10)

    tk.Label(frame_right, text="Futuro", bg="#2b2b3c", fg="white").pack()

    # ===============================
    # FUNCIONES
    # ===============================
    def cargar(datos):
        tabla.delete(*tabla.get_children())

        hoy = datetime.now()
        limite = hoy + timedelta(days=30)

        for fila in datos:
            fecha = fila[5]
            stock = fila[2]

            tag = ""

            try:
                fecha_dt = datetime.strptime(str(fecha), "%Y-%m-%d")

                if stock <= 5:
                    tag = "bajo"
                elif fecha_dt <= limite:
                    tag = "caducar"

            except:
                pass

            tabla.insert("", tk.END, values=fila[:6], tags=(tag,))

        actualizar_alertas()

    def mostrar():
        cargar(obtener_medicamentos())

    def guardar():
        insertar_medicamento(
            entry_nombre.get(),
            int(entry_stock.get()),
            float(entry_compra.get()),
            float(entry_venta.get()),
            entry_fecha.get(),
            combo_sintoma.get()
        )
        mostrar()

    def buscar():
        cargar(buscar_medicamentos(entry_buscar.get()))

    def buscar_sintoma():
        cargar(buscar_por_sintoma(combo_sintoma.get()))

    def eliminar():
        sel = tabla.selection()
        if sel:
            id = tabla.item(sel)["values"][0]
            eliminar_medicamento(id)
            mostrar()

    def vender():
        sel = tabla.selection()
        if sel:
            id = tabla.item(sel)["values"][0]
            vender_medicamento(id, 1)
            mostrar()

    def stock_bajo():
        cargar(obtener_stock_bajo())

    def por_caducar():
        cargar(obtener_por_caducar())

    # ===============================
    # BOTONES ABAJO
    # ===============================
    frame_bottom = tk.Frame(ventana, bg="#1e1e2f")
    frame_bottom.grid(row=1, column=1)

    def boton(txt, cmd, color):
        tk.Button(frame_bottom, text=txt, command=cmd,
                  bg=color, fg="white", padx=8).pack(side="left", padx=4)

    boton("Mostrar", mostrar, "#2196F3")
    boton("Guardar", guardar, "#4CAF50")
    boton("Buscar", buscar, "#9C27B0")
    boton("Por Síntoma", buscar_sintoma, "#FF9800")
    boton("Stock Bajo", stock_bajo, "#f44336")
    boton("Por Caducar", por_caducar, "#795548")
    boton("Eliminar", eliminar, "#607D8B")
    boton("Vender", vender, "#009688")
    boton("Gráfica", abrir_grafica, "#3F51B5")

    mostrar()