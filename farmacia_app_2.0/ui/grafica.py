import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from db import ventas_por_medicamento, archivar_ventas_semana, obtener_historial_por_semanas

def abrir_grafica():
    ventana = tk.Toplevel()
    ventana.title(" Análisis de Ventas - Farmacia")
    ventana.geometry("900x750")
    ventana.configure(bg="#0f172a") # Slate 900 background

    frame_botones = tk.Frame(ventana, bg="#0f172a")
    frame_botones.pack(pady=(15, 0))

    def cerrar_semana():
        if messagebox.askyesno("Cerrar Semana", "¿Deseas cerrar la semana? Esto archivará las ventas y reiniciará la gráfica a cero."):
            if archivar_ventas_semana():
                messagebox.showinfo("Éxito", "Semana cerrada exitosamente.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudieron archivar los datos.")

    btn_semana = tk.Button(frame_botones, text="Cerrar Semana y Archivar", font=("Segoe UI", 11, "bold"), bg="#14b8a6", fg="white", cursor="hand2", bd=0, command=cerrar_semana)
    btn_semana.pack(side="left", padx=10, ipadx=10, ipady=5)

    def ver_historial():
        ventana_h = tk.Toplevel(ventana)
        ventana_h.title("Historial de Ventas por Semanas")
        ventana_h.geometry("800x450")
        ventana_h.configure(bg="#0f172a")
        
        tk.Label(ventana_h, text=" Historial de Ventas Agrupado por Semana", font=("Segoe UI", 16, "bold"), bg="#0f172a", fg="#38bdf8").pack(pady=15)
        
        from tkinter import ttk
        
        frame_tabla = tk.Frame(ventana_h, bg="#0f172a")
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        columnas = ("Semana de Corte", "Medicamento", "Unidades Vendidas", "Total Ingreso ($)")
        tabla_h = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        ancho_cols = {"Semana de Corte": 150, "Medicamento": 250, "Unidades Vendidas": 150, "Total Ingreso ($)": 150}
        for col in columnas:
            tabla_h.heading(col, text=col.upper())
            tabla_h.column(col, width=ancho_cols[col], anchor="center" if col != "Medicamento" else "w")
            
        tabla_h.pack(side="left", fill="both", expand=True)
        
        scroll_h = ttk.Scrollbar(frame_tabla, command=tabla_h.yview)
        scroll_h.pack(side="right", fill="y")
        tabla_h.config(yscrollcommand=scroll_h.set)
        
        datos_historial = obtener_historial_por_semanas()
        for fila in datos_historial:
            # fila = (semana, nombre, total_vendido, total_ingreso)
            valores = (fila[0], fila[1], fila[2], f"${fila[3]:.2f}" if fila[3] else "$0.00")
            tabla_h.insert("", tk.END, values=valores)

    btn_historial = tk.Button(frame_botones, text=" Ver Historial", font=("Segoe UI", 11, "bold"), bg="#8b5cf6", fg="white", cursor="hand2", bd=0, command=ver_historial)
    btn_historial.pack(side="left", padx=10, ipadx=10, ipady=5)

    datos = ventas_por_medicamento()

    if not datos:
        tk.Label(ventana, text="No hay ventas registradas todavía.", font=("Segoe UI", 16, "bold"), bg="#0f172a", fg="#94a3b8").pack(pady=50)
        return

    nombres = [d[0] for d in datos]
    cantidades = [d[1] for d in datos]
    ingresos = [float(d[2]) if d[2] else 0 for d in datos]

    # Estilo moderno de la gráfica
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7))
    fig.patch.set_facecolor('#0f172a') # Fondo de la figura
    
    # Subplot 1: Cantidades Vendidas
    ax1.set_facecolor('#1e293b')
    barras_cant = ax1.bar(nombres, cantidades, color="#0ea5e9", edgecolor="#38bdf8", linewidth=1.5, alpha=0.9)
    ax1.set_title("UNIDADES VENDIDAS POR MEDICAMENTO", fontsize=12, fontweight="bold", color="#e2e8f0", pad=10)
    ax1.set_ylabel("Cantidad", fontsize=10, color="#94a3b8")
    
    # Subplot 2: Ingresos Generados
    ax2.set_facecolor('#1e293b')
    barras_ing = ax2.bar(nombres, ingresos, color="#10b981", edgecolor="#34d399", linewidth=1.5, alpha=0.9)
    ax2.set_title("INGRESOS GENERADOS POR MEDICAMENTO ($)", fontsize=12, fontweight="bold", color="#e2e8f0", pad=10)
    ax2.set_xlabel("Medicamentos", fontsize=10, color="#94a3b8")
    ax2.set_ylabel("Dinero ($)", fontsize=10, color="#94a3b8")

    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#475569')
        ax.spines['bottom'].set_color('#475569')
        ax.tick_params(axis='x', colors='#cbd5e1', rotation=45 if len(nombres) > 5 else 0)
        ax.tick_params(axis='y', colors='#cbd5e1')
        ax.grid(axis='y', linestyle='--', alpha=0.3, color='#94a3b8')

    # Etiquetas encima de las barras ax1
    for barra in barras_cant:
        yval = barra.get_height()
        ax1.text(barra.get_x() + barra.get_width()/2, yval, int(yval), ha='center', va='bottom', fontsize=9, fontweight="bold", color="#f8fafc")

    # Etiquetas encima de las barras ax2
    for barra in barras_ing:
        yval = barra.get_height()
        ax2.text(barra.get_x() + barra.get_width()/2, yval, f"${yval:.2f}", ha='center', va='bottom', fontsize=9, fontweight="bold", color="#f8fafc")

    plt.tight_layout()

    # Integrar con Tkinter
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)