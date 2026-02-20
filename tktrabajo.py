from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Variables y función principal
registros = []
monto = 0.0

def registrar_movimiento(cantidad):
    fecha = datetime.now()
    registros.append((cantidad, fecha))
    # return fecha   

# Funciones para los botones

def actualizar_saldo():
    label_saldo.config(text=f"Saldo actual: ${monto:,.2f}")

def ingresar():
    try:
        ingreso = float(entry_monto.get())
        if ingreso > 0:
            global monto
            monto += ingreso
            registrar_movimiento(ingreso)
            actualizar_saldo()
            messagebox.showinfo("Éxito", "Se ha ingresado con éxito!")
            entry_monto.delete(0, tk.END)
        else:
            messagebox.showwarning("Atención", "El ingreso debe ser mayor que cero!")
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número válido por favor")

def retirar():
    try:
        retiro = float(entry_monto.get())
        global monto
        if retiro > 0:
            if retiro <= monto:
                monto -= retiro
                registrar_movimiento(-retiro)
                actualizar_saldo()
                messagebox.showinfo("Éxito", "Se ha retirado con éxito!")
                print(f"Saldo actual: ${monto:,.2f}")   # ← lo dejamos en consola si quieres verlo ahí también
                entry_monto.delete(0, tk.END)
            else:
                messagebox.showwarning("Saldo insuficiente", f"Disponible: ${monto:,.2f}")
        else:
            messagebox.showwarning("Atención", "El monto a retirar debe ser mayor que cero.")
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número válido.")

def ver_movimientos():
    if not registros:
        messagebox.showinfo("Reporte", "Todavía no hay movimientos registrados.")
        return

    texto = "Movimientos registrados:\n\n"
    for cantidad, fecha in registros:
        agenda = fecha.strftime("%d/%m/%Y %H:%M")
        if cantidad > 0:
            texto += f"Ingreso:  +${cantidad:,.2f}  | {agenda}\n"
        else:
            texto += f"Retiro:   -${abs(cantidad):,.2f}   | {agenda}\n"
    
    texto += f"\nSaldo actual: ${monto:,.2f}\n"
    
    # Ventana emergente con el reporte
    ventana_reporte = tk.Toplevel()
    ventana_reporte.title("Reporte de movimientos")
    ventana_reporte.geometry("500x400")
    
    tk.Label(ventana_reporte, text="Reporte", font=("Arial", 14, "bold")).pack(pady=10)
    texto_widget = tk.Text(ventana_reporte, font=("Consolas", 11), wrap="word")
    texto_widget.insert(tk.END, texto)
    texto_widget.config(state="disabled")
    texto_widget.pack(padx=15, pady=10, fill="both", expand=True)

# Ventana principal 
ventana = tk.Tk()
ventana.title("Contador Personal")
ventana.geometry("420x450")
ventana.configure(bg="#f8f9fa")

# Título
tk.Label(ventana, text="Bienvenido a su contador", font=("Arial", 16, "bold"), bg="#f8f9fa").pack(pady=15)

# Saldo
label_saldo = tk.Label(ventana, text=f"Saldo actual: ${monto:,.2f}", font=("Arial", 18, "bold"), fg="#0066cc", bg="#f8f9fa")
label_saldo.pack(pady=20)

# Entrada de monto
tk.Label(ventana, text="Monto:", font=("Arial", 12), bg="#f8f9fa").pack()
entry_monto = tk.Entry(ventana, font=("Arial", 14), width=15, justify="center")
entry_monto.pack(pady=10)

# Botones
frame_botones = tk.Frame(ventana, bg="#f8f9fa")
frame_botones.pack(pady=20)

tk.Button(frame_botones, text="1. Ingresar", font=("Arial", 11, "bold"), bg="#28a745", fg="white", width=14, command=ingresar).grid(row=0, column=0, padx=10, pady=8)
tk.Button(frame_botones, text="3. Retirar",   font=("Arial", 11, "bold"), bg="#dc3545", fg="white", width=14, command=retirar).grid(row=0, column=1, padx=10, pady=8)
tk.Button(frame_botones, text="2. Ver reporte", font=("Arial", 11, "bold"), bg="#6c757d", fg="white", width=14, command=ver_movimientos).grid(row=1, column=0, columnspan=2, pady=8)
tk.Button(frame_botones, text="4. Salir",     font=("Arial", 11, "bold"), bg="#343a40", fg="white", width=14, command=ventana.quit).grid(row=2, column=0, columnspan=2, pady=8)

# Iniciar
actualizar_saldo()
ventana.mainloop()