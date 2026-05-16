import tkinter as tk

def abrir_inventario():
    from ui.inventario import abrir_inventario
    abrir_inventario()

def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Farmacia")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Sistema Farmacia", font=("Arial", 16)).pack(pady=20)

    tk.Button(ventana, text="Inventario", width=20, command=abrir_inventario).pack(pady=10)

    ventana.mainloop()