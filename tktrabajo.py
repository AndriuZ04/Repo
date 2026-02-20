from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import json
import os

# ── Archivo donde se guardan los datos ──
DATA_FILE = "contador_datos.json"

# ── Credenciales fijas (cámbialas después si quieres) ──
USUARIO_CORRECTO = "andriu"
CONTRASENA_CORRECTA = "1234"

# Variables globales
registros = []
monto = 0.0

def registrar_movimiento(cantidad):
    fecha = datetime.now()
    registros.append((cantidad, fecha))

def actualizar_saldo():
    label_saldo.config(text=f"Saldo actual: ${monto:,.2f}")

def guardar_datos():
    datos = {
        "monto": monto,
        "registros": [(cant, fecha.isoformat()) for cant, fecha in registros]
    }
    with open(DATA_FILE, "w") as f:
        json.dump(datos, f, indent=4)

def cargar_datos():
    global monto, registros
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                datos = json.load(f)
                monto = datos.get("monto", 0.0)
                registros = [(cant, datetime.fromisoformat(fecha_str)) for cant, fecha_str in datos.get("registros", [])]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")

# ── Funciones de botones (igual que antes, solo agrego guardar al final de operaciones) ──

def ingresar():
    try:
        ingreso = float(entry_monto.get())
        if ingreso > 0:
            global monto
            monto += ingreso
            registrar_movimiento(ingreso)
            actualizar_saldo()
            guardar_datos()  # ← guarda después de cada cambio
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
                guardar_datos()  # ← guarda después de cada cambio
                messagebox.showinfo("Éxito", "Se ha retirado con éxito!")
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
    
    ventana_reporte = tk.Toplevel()
    ventana_reporte.title("Reporte de movimientos")
    ventana_reporte.geometry("500x400")
    
    tk.Label(ventana_reporte, text="Reporte", font=("Arial", 14, "bold")).pack(pady=10)
    texto_widget = tk.Text(ventana_reporte, font=("Consolas", 11), wrap="word")
    texto_widget.insert(tk.END, texto)
    texto_widget.config(state="disabled")
    texto_widget.pack(padx=15, pady=10, fill="both", expand=True)

def pedir_contrasena():
    """Ventana pequeña para pedir contraseña y verificarla"""
    ventana_pass = tk.Toplevel()
    ventana_pass.title("Verificar contraseña")
    ventana_pass.geometry("350x180")
    ventana_pass.configure(bg="#f8f9fa")
    
    tk.Label(ventana_pass, text="Ingresa tu contraseña para confirmar:", 
             font=("Arial", 12), bg="#f8f9fa").pack(pady=15)
    
    entry_pass = tk.Entry(ventana_pass, font=("Arial", 12), width=20, show="*")
    entry_pass.pack(pady=10)
    
    resultado = [False]  # lista para poder modificar desde adentro
    
    def verificar():
        if entry_pass.get() == CONTRASENA_CORRECTA:
            resultado[0] = True
            ventana_pass.destroy()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
            ventana_pass.destroy()
    
    tk.Button(ventana_pass, text="Confirmar", font=("Arial", 11, "bold"), 
              bg="#0066cc", fg="white", command=verificar).pack(pady=10)
    
    ventana_pass.wait_window()  # espera hasta que se cierre
    return resultado[0]

def eliminar_movimiento():
    if not registros:
        messagebox.showinfo("Información", "No hay movimientos para eliminar.")
        return
    
    if not pedir_contrasena():
        return  # si contraseña mala → salir
    
    # Mostrar lista numerada en una ventana
    ventana_elim = tk.Toplevel()
    ventana_elim.title("Eliminar movimiento")
    ventana_elim.geometry("600x500")
    
    tk.Label(ventana_elim, text="Selecciona el número del movimiento a eliminar:", 
             font=("Arial", 16, "bold")).pack(pady=12)
    
    texto = tk.Text(ventana_elim, font=("Consolas", 11), height=15)
    texto.pack(padx=15, pady=10, fill="both", expand=True)
    
    for i, (cantidad, fecha) in enumerate(registros, 1):
        agenda = fecha.strftime("%d/%m/%Y %H:%M")
        if cantidad > 0:
            linea = f"{i}. Ingreso: +${cantidad:,.2f} | {agenda}\n"
        else:
            linea = f"{i}. Retiro:  -${abs(cantidad):,.2f} | {agenda}\n"
        texto.insert(tk.END, linea)
    
    texto.config(state="disabled")
    
    tk.Label(ventana_elim, text="Número del movimiento:", font=("Arial", 11)).pack(pady=5)
    entry_num = tk.Entry(ventana_elim, width=10, justify="center")
    entry_num.pack(pady=5)
    
    def borrar_seleccionado():
        try:
            num = int(entry_num.get())
            if 1 <= num <= len(registros):
                eliminado = registros.pop(num - 1)
                if eliminado[0] > 0:
                    global monto
                    monto -= eliminado[0]  # restar el ingreso que se elimina
                else:
                    monto += abs(eliminado[0])  # sumar de vuelta el retiro eliminado
                actualizar_saldo()
                guardar_datos()
                messagebox.showinfo("Éxito", "Movimiento eliminado correctamente.")
                ventana_elim.destroy()
            else:
                messagebox.showwarning("Error", "Número fuera de rango.")
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido.")
    
    tk.Button(ventana_elim, text="Eliminar seleccionado", bg="#d62638", fg="white", 
              command=borrar_seleccionado).pack(pady=18)
    
def borrar_todo():
    global monto, registros
    if not registros and monto == 0:
        messagebox.showinfo("Información", "No hay datos para borrar.")
        return
    
    if not pedir_contrasena():
        return
    
    if messagebox.askyesno("Confirmar", "¿Realmente quieres borrar TODOS los movimientos y poner saldo en 0?"):
        monto = 0.0
        registros = []
        actualizar_saldo()
        guardar_datos()
        messagebox.showinfo("Éxito", "Todo ha sido borrado.")

def salir():
    if messagebox.askyesno("Salir", "¿Seguro que quieres salir?"):
        guardar_datos()
        ventana.destroy()

# ── Ventana de login ──

def verificar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    
    if usuario == USUARIO_CORRECTO and contrasena == CONTRASENA_CORRECTA:
        ventana_login.destroy()
        iniciar_contador()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def iniciar_contador():
    global ventana, label_saldo, entry_monto
    
    ventana = tk.Tk()
    ventana.title("Contador Personal")
    ventana.geometry("420x550")
    ventana.configure(bg="#f8f9fa")
    
    # Cargar datos guardados
    cargar_datos()
    
    tk.Label(ventana, text="Bienvenido a su contador", font=("Arial", 16, "bold"), bg="#f8f9fa").pack(pady=15)
    
    label_saldo = tk.Label(ventana, text=f"Saldo actual: ${monto:,.2f}", font=("Arial", 18, "bold"), fg="#0066cc", bg="#f8f9fa")
    label_saldo.pack(pady=20)
    
    tk.Label(ventana, text="Monto:", font=("Arial", 12), bg="#f8f9fa").pack()
    entry_monto = tk.Entry(ventana, font=("Arial", 14), width=15, justify="center")
    entry_monto.pack(pady=10)
    
    frame_botones = tk.Frame(ventana, bg="#f8f9fa")
    frame_botones.pack(pady=20)
    
    tk.Button(frame_botones, text="1. Ingresar", font=("Arial", 11, "bold"), bg="#28a745", fg="white", width=14, command=ingresar).grid(row=0, column=0, padx=10, pady=8)
    tk.Button(frame_botones, text="2. Retirar",   font=("Arial", 11, "bold"), bg="#dc3545", fg="white", width=14, command=retirar).grid(row=0, column=1, padx=10, pady=8)
    tk.Button(frame_botones, text="3. Ver reporte", font=("Arial", 11, "bold"), bg="#6c757d", fg="white", width=14, command=ver_movimientos).grid(row=1, column=0, columnspan=2, pady=8)
    tk.Button(frame_botones, text="4. Eliminar movimiento", font=("Arial", 11, "bold"), bg="#ff9800", fg="white", width=20, command=eliminar_movimiento).grid(row=2, column=0, columnspan=2, pady=8)
    tk.Button(frame_botones, text="5. Borrar todo", font=("Arial", 11, "bold"), bg="#f44336", fg="white", width=20, command=borrar_todo).grid(row=3, column=0, columnspan=2, pady=8)
    tk.Button(frame_botones, text="6. Salir", font=("Arial", 11, "bold"), bg="#343a40", fg="white", width=14, command=salir).grid(row=4, column=0, columnspan=2, pady=8)

    actualizar_saldo()
    ventana.protocol("WM_DELETE_WINDOW", salir)  # guarda si cierra con la X
    ventana.mainloop()

# ── Ventana de login ──
ventana_login = tk.Tk()
ventana_login.title("Login - Contador Personal")
ventana_login.geometry("400x300")
ventana_login.configure(bg="#f8f9fa")

tk.Label(ventana_login, text="Iniciar Sesión", font=("Arial", 16, "bold"), bg="#f8f9fa").pack(pady=20)

tk.Label(ventana_login, text="Usuario:", font=("Arial", 12), bg="#f8f9fa").pack()
entry_usuario = tk.Entry(ventana_login, font=("Arial", 12), width=20)
entry_usuario.pack(pady=5)

tk.Label(ventana_login, text="Contraseña:", font=("Arial", 12), bg="#f8f9fa").pack()
entry_contrasena = tk.Entry(ventana_login, font=("Arial", 12), width=20, show="*")
entry_contrasena.pack(pady=5)

tk.Button(ventana_login, text="Entrar", font=("Arial", 12, "bold"), bg="#0066cc", fg="white", width=15, command=verificar_login).pack(pady=30)

ventana_login.mainloop()