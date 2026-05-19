import tkinter as tk

def abrir_inventario():
    from ui.inventario import abrir_inventario
    abrir_inventario()

def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Farmacia - Dashboard Principal")
    ventana.geometry("500x350")
    ventana.configure(bg="#f4f6f9")
    
    # Header
    header = tk.Frame(ventana, bg="#2c3e50", height=80)
    header.pack(fill="x")
    
    titulo = tk.Label(header, text=" Sistema de Farmacia", font=("Segoe UI", 20, "bold"), bg="#2c3e50", fg="white")
    titulo.pack(pady=20)

    # Contenedor central
    frame_centro = tk.Frame(ventana, bg="#f4f6f9")
    frame_centro.pack(expand=True)

    # Estilos de botón
    btn_bg = "#3498db"
    btn_hover = "#2980b9"

    btn_inventario = tk.Button(
        frame_centro, text=" Abrir Inventario", font=("Segoe UI", 12, "bold"), 
        bg=btn_bg, fg="white", width=25, height=2, bd=0, cursor="hand2",
        command=abrir_inventario
    )
    btn_inventario.pack(pady=20)

    # Funciones de animación (Hover)
    def on_enter(e):
        e.widget['background'] = btn_hover
    def on_leave(e):
        e.widget['background'] = btn_bg

    btn_inventario.bind("<Enter>", on_enter)
    btn_inventario.bind("<Leave>", on_leave)

    ventana.mainloop()