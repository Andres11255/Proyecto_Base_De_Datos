import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta

from db import (
    insertar_medicamento,
    obtener_medicamentos,
    buscar_medicamentos,
    buscar_por_sintoma,
    eliminar_medicamento,
    vender_medicamento,
    obtener_stock_bajo,
    obtener_por_caducar,
    obtener_por_caducar,
    agregar_stock_medicamento
)

from ui.grafica import abrir_grafica


def abrir_inventario():
    ventana = tk.Tk()
    ventana.title("Sistema FarmaCut")
    ventana.geometry("1300x750")
    ventana.configure(bg="#0f172a") # Slate 900
    
    # Fuentes
    font_title = ("Segoe UI", 16, "bold")
    font_label = ("Segoe UI", 10, "bold")
    font_entry = ("Segoe UI", 11)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=4)
    ventana.rowconfigure(1, weight=1)

    # ===============================
    # HEADER / ALERTAS
    # ===============================
    header_frame = tk.Frame(ventana, bg="#1e293b", height=60)
    header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
    header_frame.pack_propagate(False)
    
    titulo = tk.Label(header_frame, text="✚ Sistema FarmaCut", font=("Segoe UI", 20, "bold"), bg="#1e293b", fg="#e2e8f0")
    titulo.place(relx=0.5, rely=0.5, anchor="center")

    alerta = tk.Label(
        header_frame,
        text="",
        bg="#1e293b",
        fg="#f59e0b",
        font=("Segoe UI", 12, "bold")
    )
    alerta.pack(side="right", padx=20, pady=15)

    def actualizar_alertas():
        bajos = len(obtener_stock_bajo())
        caducar = len(obtener_por_caducar())
        alerta.config(
            text=f"⚠ Alertas: Stock bajo ({bajos}) | Por caducar ({caducar})"
        )

    # ===============================
    # PANEL IZQUIERDO (FORMULARIO)
    # ===============================
    frame_left = tk.Frame(ventana, bg="#1e293b", bd=0, highlightbackground="#334155", highlightthickness=1)
    frame_left.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
    
    tk.Label(frame_left, text="Registrar Medicamento", font=font_title, bg="#1e293b", fg="#38bdf8").pack(pady=(20, 10))

    def campo(texto):
        frame_input = tk.Frame(frame_left, bg="#1e293b")
        frame_input.pack(fill="x", padx=20, pady=5)
        tk.Label(frame_input, text=texto, fg="#94a3b8", bg="#1e293b", font=font_label).pack(anchor="w")
        entrada = tk.Entry(frame_input, font=font_entry, bg="#0f172a", fg="white", insertbackground="white", relief="flat", highlightbackground="#334155", highlightthickness=1, highlightcolor="#38bdf8")
        entrada.pack(fill="x", pady=2, ipady=4)
        return entrada

    entry_nombre = campo("Nombre del Medicamento")
    entry_stock = campo("Cantidad en Stock")
    entry_compra = campo("Precio de Compra ($)")
    entry_venta = campo("Precio de Venta ($)")
    entry_fecha = campo("Fecha Caducidad (YYYY-MM-DD)")

    frame_sint = tk.Frame(frame_left, bg="#1e293b")
    frame_sint.pack(fill="x", padx=20, pady=5)
    tk.Label(frame_sint, text="Malestar / Síntoma", fg="#94a3b8", bg="#1e293b", font=font_label).pack(anchor="w")
    opciones_sintomas = [
        "Dolor", "Tos", "Alergia", "Estómago", "Gripa", "Fiebre",
        "Dolor y Fiebre", "Alergias", "Tos y Gripe", 
        "Infecciones Bacterianas", "Infecciones Virales", "Infecciones por Hongos", 
        "Problemas Estomacales", "Hipertensión y Corazón", "Diabetes", 
        "Ansiedad y Depresión", "Cuidado Ocular", "Cuidado de la Piel", 
        "Vitaminas y Suplementos", "Antiparasitarios", "Tiroides y Hormonas", "Otro"
    ]
    combo_sintoma = ttk.Combobox(frame_sint, values=opciones_sintomas, font=font_entry, state="readonly")
    combo_sintoma.pack(fill="x", pady=2, ipady=4)

    # Botones del Formulario
    btn_agregar = tk.Button(frame_left, text="➕ Agregar Medicamento", font=("Segoe UI", 11, "bold"), bg="#10b981", fg="white", cursor="hand2", bd=0, command=lambda: guardar())
    btn_agregar.pack(fill="x", padx=20, pady=(15, 5), ipady=6)

    def on_enter_a(e): e.widget['background'] = '#059669'
    def on_leave_a(e): e.widget['background'] = '#10b981'
    btn_agregar.bind("<Enter>", on_enter_a)
    btn_agregar.bind("<Leave>", on_leave_a)

    def cargar_datos_formulario():
        nombre_busqueda = entry_nombre.get().strip()
        if not nombre_busqueda:
            messagebox.showwarning("Atención", "Escribe el nombre en la primera casilla para buscar toda su información.")
            return
            
        res = buscar_medicamentos(nombre_busqueda)
        if res:
            med = res[0]
            limpiar_campos()
            entry_nombre.insert(0, str(med[1]))
            entry_stock.insert(0, str(med[2]))
            entry_compra.insert(0, str(med[3]))
            entry_venta.insert(0, str(med[4]))
            entry_fecha.insert(0, str(med[5]))
            try:
                combo_sintoma.set(str(med[6]))
            except IndexError:
                pass
        else:
            messagebox.showerror("No encontrado", "No existe un medicamento con ese nombre en el sistema.")

    btn_cargar = tk.Button(frame_left, text="🔍 Buscar y Cargar Info", font=("Segoe UI", 10, "bold"), bg="#3b82f6", fg="white", cursor="hand2", bd=0, command=cargar_datos_formulario)
    btn_cargar.pack(fill="x", padx=20, pady=(0, 5), ipady=5)

    def on_enter_c(e): e.widget['background'] = '#2563eb'
    def on_leave_c(e): e.widget['background'] = '#3b82f6'
    btn_cargar.bind("<Enter>", on_enter_c)
    btn_cargar.bind("<Leave>", on_leave_c)

    def limpiar_campos():
        entry_nombre.delete(0, tk.END)
        entry_stock.delete(0, tk.END)
        entry_compra.delete(0, tk.END)
        entry_venta.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)
        combo_sintoma.set("")

    btn_limpiar = tk.Button(frame_left, text="✨ Limpiar Datos", font=("Segoe UI", 10, "bold"), bg="#475569", fg="white", cursor="hand2", bd=0, command=limpiar_campos)
    btn_limpiar.pack(fill="x", padx=20, pady=(0, 5), ipady=5)

    def on_enter_l(e): e.widget['background'] = '#64748b'
    def on_leave_l(e): e.widget['background'] = '#475569'
    btn_limpiar.bind("<Enter>", on_enter_l)
    btn_limpiar.bind("<Leave>", on_leave_l)

    # Buscador en panel izquierdo
    tk.Frame(frame_left, bg="#334155", height=2).pack(fill="x", padx=20, pady=20) # Separador
    tk.Label(frame_left, text="Búsqueda Rápida", font=font_title, bg="#1e293b", fg="#38bdf8").pack(pady=(0, 10))
    
    # Búsqueda por Nombre
    frame_buscar = tk.Frame(frame_left, bg="#1e293b")
    frame_buscar.pack(fill="x", padx=20, pady=5)
    
    entry_buscar = tk.Entry(frame_buscar, font=font_entry, bg="#0f172a", fg="white", insertbackground="white", relief="flat", highlightbackground="#334155", highlightthickness=1)
    entry_buscar.pack(side="left", fill="x", expand=True, ipady=4)

    def evento_buscar(e): buscar()
    entry_buscar.bind("<Return>", evento_buscar)

    btn_buscar = tk.Button(frame_buscar, text="🔍 Nombre", font=("Segoe UI", 10, "bold"), bg="#8b5cf6", fg="white", cursor="hand2", bd=0, command=lambda: buscar())
    btn_buscar.pack(side="right", padx=(5,0), ipadx=10, ipady=4)

    # Búsqueda por Síntoma
    frame_buscar_sint = tk.Frame(frame_left, bg="#1e293b")
    frame_buscar_sint.pack(fill="x", padx=20, pady=5)
    
    entry_buscar_sint = tk.Entry(frame_buscar_sint, font=font_entry, bg="#0f172a", fg="white", insertbackground="white", relief="flat", highlightbackground="#334155", highlightthickness=1)
    entry_buscar_sint.pack(side="left", fill="x", expand=True, ipady=4)
    
    def buscar_s_texto():
        cargar(buscar_por_sintoma(entry_buscar_sint.get()))
        
    def evento_buscar_sint(e): buscar_s_texto()
    entry_buscar_sint.bind("<Return>", evento_buscar_sint)

    btn_buscar_sint = tk.Button(frame_buscar_sint, text="🔍 Síntoma", font=("Segoe UI", 10, "bold"), bg="#f59e0b", fg="white", cursor="hand2", bd=0, command=buscar_s_texto)
    btn_buscar_sint.pack(side="right", padx=(5,0), ipadx=10, ipady=4)

    # ===============================
    # TABLA CENTRAL
    # ===============================
    frame_center = tk.Frame(ventana, bg="#0f172a")
    frame_center.grid(row=1, column=1, sticky="nsew", padx=(0, 20), pady=20)

    # Estilo Treeview Premium
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", 
                    background="#1e293b",
                    foreground="white",
                    rowheight=30,
                    fieldbackground="#1e293b",
                    font=("Segoe UI", 10),
                    borderwidth=0)
    style.map('Treeview', background=[('selected', '#38bdf8')])
    style.configure("Treeview.Heading",
                    background="#334155",
                    foreground="white",
                    font=("Segoe UI", 11, "bold"),
                    relief="flat")
    style.map("Treeview.Heading", background=[('active', '#475569')])

    # Estilo Scrollbar Moderno
    style.configure("Vertical.TScrollbar",
                    background="#334155",
                    troughcolor="#0f172a",
                    bordercolor="#0f172a",
                    arrowcolor="#38bdf8",
                    relief="flat",
                    borderwidth=0)
    style.map("Vertical.TScrollbar",
              background=[('active', '#475569')],
              arrowcolor=[('active', '#ffffff')])

    # ===============================
    # BOTONERA SUPERIOR (SOBRE LA TABLA)
    # ===============================
    frame_actions = tk.Frame(frame_center, bg="#0f172a")
    frame_actions.pack(fill="x", pady=(0, 10))

    scrollbar = ttk.Scrollbar(frame_center)
    scrollbar.pack(side="right", fill="y")

    columnas = ("ID", "Nombre", "Stock", "Compra", "Venta", "Caducidad")
    tabla = ttk.Treeview(frame_center, columns=columnas, show="headings", yscrollcommand=scrollbar.set)
    scrollbar.config(command=tabla.yview)

    ancho_cols = {"ID": 50, "Nombre": 250, "Stock": 80, "Compra": 100, "Venta": 100, "Caducidad": 120}
    for col in columnas:
        tabla.heading(col, text=col.upper())
        tabla.column(col, width=ancho_cols[col], anchor="center" if col != "Nombre" else "w")

    tabla.pack(fill="both", expand=True)

    tabla.tag_configure("bajo", background="#ef4444")
    tabla.tag_configure("caducar", background="#eab308", foreground="black")

    # ===============================
    # FUNCIONES
    # ===============================
    def cargar(datos):
        tabla.delete(*tabla.get_children())
        hoy = datetime.now()
        limite = hoy + timedelta(days=30)

        for i, fila in enumerate(datos, start=1):
            fecha = fila[5]
            stock = fila[2]
            tag = ""
            try:
                fecha_dt = datetime.strptime(str(fecha), "%Y-%m-%d")
                if stock <= 5:
                    tag = "bajo"
                elif fecha_dt <= limite:
                    tag = "caducar"
            except: pass

            # fila[0] es el ID real de BD, lo pasamos al final para no mostrarlo pero mantenerlo
            valores = (i, fila[1], fila[2], fila[3], fila[4], fila[5], fila[0])
            tabla.insert("", tk.END, values=valores, tags=(tag,))

        actualizar_alertas()

    def mostrar():
        cargar(obtener_medicamentos())

    def guardar():
        try:
            nombre = entry_nombre.get()
            stock = entry_stock.get()
            compra = entry_compra.get()
            venta = entry_venta.get()
            fecha = entry_fecha.get()
            sintoma = combo_sintoma.get()

            if not nombre or not stock or not compra or not venta or not fecha or not sintoma:
                messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos del formulario.")
                return

            insertar_medicamento(
                nombre,
                int(stock),
                float(compra),
                float(venta),
                fecha,
                sintoma
            )
            mostrar()
            limpiar_campos()
            messagebox.showinfo("Éxito", f"¡El medicamento '{nombre}' se agregó correctamente al inventario!")
        except ValueError:
            messagebox.showerror("Error de Datos", "Por favor asegúrate de que el Stock y los Precios sean números.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el medicamento: {e}")

    def buscar():
        cargar(buscar_medicamentos(entry_buscar.get()))

    def eliminar():
        sel = tabla.selection()
        if sel:
            id = tabla.item(sel)["values"][6]
            eliminar_medicamento(id)
            mostrar()

    def vender():
        sel = tabla.selection()
        if sel:
            id_med = tabla.item(sel)["values"][6]
            nombre_med = tabla.item(sel)["values"][1]
            cantidad = simpledialog.askinteger("Vender Medicamento", f"¿Cuántas unidades de '{nombre_med}' deseas vender?", minvalue=1)
            if cantidad and cantidad > 0:
                vender_medicamento(id_med, cantidad)
                mostrar()
        else:
            messagebox.showwarning("Selección requerida", "Selecciona un medicamento de la tabla primero.")

    def anadir_surtido():
        sel = tabla.selection()
        if sel:
            id_med = tabla.item(sel)["values"][6]
            nombre_med = tabla.item(sel)["values"][1]
            cantidad = simpledialog.askinteger("Añadir Surtido", f"¿Cuántas unidades de '{nombre_med}' llegaron?")
            if cantidad and cantidad > 0:
                agregar_stock_medicamento(id_med, cantidad)
                mostrar()
                messagebox.showinfo("Stock Actualizado", f"Se añadieron {cantidad} unidades a {nombre_med}.")
        else:
            messagebox.showwarning("Selección requerida", "Selecciona un medicamento de la tabla primero.")


    def stock_bajo():
        cargar(obtener_stock_bajo())

    def por_caducar():
        cargar(obtener_por_caducar())

    def boton_animado(parent, txt, cmd, color_base, color_hover):
        btn = tk.Button(
            parent, text=txt, command=cmd,
            bg=color_base, fg="white", font=("Segoe UI", 10, "bold"),
            padx=15, pady=8, bd=0, cursor="hand2"
        )
        def on_enter(e): e.widget['background'] = color_hover
        def on_leave(e): e.widget['background'] = color_base
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    # old buscar_sintoma removed

    def buscar_sintoma_dialog():
        ventana_busqueda = tk.Toplevel(ventana)
        ventana_busqueda.title("Búsqueda Inteligente")
        ventana_busqueda.geometry("350x200")
        ventana_busqueda.configure(bg="#1e293b")
        ventana_busqueda.grab_set() # Convertir en ventana modal

        tk.Label(ventana_busqueda, text="¿Qué malestar o síntoma tienes?", font=("Segoe UI", 12, "bold"), bg="#1e293b", fg="#38bdf8").pack(pady=(25, 10))

        opciones = [
            "Dolor", "Tos", "Alergia", "Estómago", "Gripa", "Fiebre",
            "Dolor y Fiebre", "Alergias", "Tos y Gripe", 
            "Infecciones Bacterianas", "Infecciones Virales", "Infecciones por Hongos", 
            "Problemas Estomacales", "Hipertensión y Corazón", "Diabetes", 
            "Ansiedad y Depresión", "Cuidado Ocular", "Cuidado de la Piel", 
            "Vitaminas y Suplementos", "Antiparasitarios", "Tiroides y Hormonas", "Otro"
        ]
        combo_busqueda = ttk.Combobox(ventana_busqueda, values=opciones, font=("Segoe UI", 11), state="readonly")
        combo_busqueda.pack(pady=5, padx=30, fill="x", ipady=4)
        
        def realizar_busqueda():
            sintoma = combo_busqueda.get()
            if sintoma:
                resultados = buscar_por_sintoma(sintoma)
                cargar(resultados)
                if not resultados:
                    messagebox.showinfo("Resultados", f"No se encontraron medicamentos para el síntoma: '{sintoma}'")
            ventana_busqueda.destroy()

        btn_buscar_dialog = tk.Button(ventana_busqueda, text="🔍 Buscar", font=("Segoe UI", 10, "bold"), bg="#f59e0b", fg="white", bd=0, cursor="hand2", command=realizar_busqueda)
        btn_buscar_dialog.pack(pady=(15, 0), ipadx=20, ipady=5)

    # Acciones de Tabla
    btn_recargar = boton_animado(frame_actions, " Recargar Todo", mostrar, "#3b82f6", "#2563eb")
    btn_recargar.pack(side="left", padx=5)
    
    btn_vender = boton_animado(frame_actions, " Vender", vender, "#0ea5e9", "#0284c7")
    btn_vender.pack(side="left", padx=5)
    
    btn_sintoma = boton_animado(frame_actions, " Buscar por Síntoma", buscar_sintoma_dialog, "#f59e0b", "#d97706")
    btn_sintoma.pack(side="left", padx=5)
    
    btn_surtido = boton_animado(frame_actions, " Añadir Surtido", anadir_surtido, "#8b5cf6", "#7c3aed")
    btn_surtido.pack(side="left", padx=5)
    
    btn_eliminar = boton_animado(frame_actions, " Eliminar", eliminar, "#ef4444", "#dc2626")
    btn_eliminar.pack(side="left", padx=5)
    
    btn_stock = boton_animado(frame_actions, " Ver Stock Bajo", stock_bajo, "#f43f5e", "#e11d48")
    btn_stock.pack(side="left", padx=5)
    
    btn_caducar = boton_animado(frame_actions, "Ver Caducado", por_caducar, "#d97706", "#b45309")
    btn_caducar.pack(side="left", padx=5)
    
    btn_grafica = boton_animado(frame_actions, " Ver Gráfica", abrir_grafica, "#6366f1", "#4f46e5")
    btn_grafica.pack(side="left", padx=5)

    mostrar()
    ventana.mainloop()