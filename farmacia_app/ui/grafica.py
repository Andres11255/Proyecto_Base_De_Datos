import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from db import ventas_por_medicamento



def abrir_grafica():
    ventana = tk.Toplevel()
    ventana.title("Gráfica de Ventas")
    ventana.geometry("700x500")

    datos = ventas_por_medicamento()

    nombres = [d[0] for d in datos]
    cantidades = [d[1] for d in datos]

    fig, ax = plt.subplots()
    ax.bar(nombres, cantidades)

    ax.set_title("Ventas por Medicamento")
    ax.set_xlabel("Medicamento")
    ax.set_ylabel("Cantidad Vendida")

    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)