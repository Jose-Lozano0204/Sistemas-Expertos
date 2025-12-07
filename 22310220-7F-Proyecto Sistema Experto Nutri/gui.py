import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from rules import recomendar_alimentos

# ------------------------------------------
# VARIABLES GLOBALES PARA GUARDAR LOS DATOS
# ------------------------------------------
usuario_nombre = ""
usuario_edad = ""

# ------------------------------------------
# DICCIONARIO DE IMÁGENES POR SÍNTOMA
# ------------------------------------------
imagenes_sintomas = {
    "Diarrea": "diarrea.jpg",
    "Vomito": "vomito.jpg",
    "Gripe": "gripe.jpg",
    "Fatiga": "fatiga.jpg",
    "Bajar de peso": "bajar.jpg",
    "Subir masa muscular": "muscular.jpg"
}

# ------------------------------------------
# FUNCIÓN PARA PREGUNTAR NOMBRE Y EDAD
# ------------------------------------------
def pedir_datos_usuario():
    limpiar_pantalla()

    titulo = tk.Label(frame, text="Bienvenido a Nutri", 
                      font=("Arial", 24, "bold"), bg="#eef7ff")
    titulo.pack(pady=10)

    subtitulo = tk.Label(frame, text="Por favor ingresa tus datos:",
                         font=("Arial", 14), bg="#eef7ff")
    subtitulo.pack(pady=5)

    # Nombre
    tk.Label(frame, text="Nombre:", font=("Arial", 12), bg="#eef7ff").pack()
    nombre_entry = tk.Entry(frame, font=("Arial", 12))
    nombre_entry.pack(pady=5)

    # Edad
    tk.Label(frame, text="Edad:", font=("Arial", 12), bg="#eef7ff").pack()
    edad_entry = tk.Entry(frame, font=("Arial", 12))
    edad_entry.pack(pady=5)

    def guardar_datos():
        global usuario_nombre, usuario_edad

        nombre = nombre_entry.get().strip()
        edad = edad_entry.get().strip()

        if nombre == "" or edad == "":
            tk.Label(frame, text="Debes llenar todos los campos.",
                     fg="red", bg="#eef7ff").pack()
            return

        if not edad.isdigit():
            tk.Label(frame, text="La edad debe ser un número.",
                     fg="red", bg="#eef7ff").pack()
            return

        usuario_nombre = nombre
        usuario_edad = edad
        mostrar_menu()

    tk.Button(frame, text="Continuar",
              font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
              command=guardar_datos).pack(pady=15)

# ------------------------------------------
# MENÚ PRINCIPAL
# ------------------------------------------
def mostrar_menu():
    limpiar_pantalla()

    titulo = tk.Label(frame, text=f"Hola {usuario_nombre}, elige tu síntoma",
                      font=("Arial", 20, "bold"), bg="#eef7ff")
    titulo.pack(pady=10)

    subtitulo = tk.Label(frame, text="Selecciona tu síntoma:",
                         font=("Arial", 14), bg="#eef7ff")
    subtitulo.pack()

    # Imagen del doctor
    img = Image.open("doctor.jpg")
    img = img.resize((250, 250))
    render = ImageTk.PhotoImage(img)

    img_label = tk.Label(frame, image=render, bg="#eef7ff")
    img_label.image = render
    img_label.pack(pady=15)

    combo = ttk.Combobox(frame, values=list(imagenes_sintomas.keys()),
                         state="readonly", font=("Arial", 12), width=25)
    combo.pack()

    tk.Button(frame, text="Obtener Recomendaciones",
              command=lambda: mostrar_recomendaciones(combo.get()),
              font=("Arial", 12, "bold"), bg="#4a90e2", fg="white",
              width=25).pack(pady=20)

    # Botón salir
    tk.Button(frame, text="Salir",
              command=ventana.quit,
              font=("Arial", 12, "bold"), bg="#d9534f", fg="white",
              width=25).pack(pady=10)

# ------------------------------------------
# MOSTRAR RECOMENDACIONES
# ------------------------------------------
def mostrar_recomendaciones(sintoma):
    limpiar_pantalla()

    titulo = tk.Label(frame, 
                      text=f"{usuario_nombre} ({usuario_edad} años)\nRecomendaciones para: {sintoma}",
                      font=("Arial", 16, "bold"),
                      bg="#eef7ff")
    titulo.pack(pady=10)

    # Imagen del síntoma
    try:
        img = Image.open(imagenes_sintomas[sintoma])
        img = img.resize((220, 220))
        render = ImageTk.PhotoImage(img)

        img_label = tk.Label(frame, image=render, bg="#eef7ff")
        img_label.image = render
        img_label.pack(pady=10)
    except:
        tk.Label(frame, text="(No hay imagen para este síntoma)",
                 bg="#eef7ff", fg="red").pack()

    # Recomendaciones
    resultado = recomendar_alimentos(sintoma)


    if not resultado:
        tk.Label(frame, text="No existen recomendaciones.",
                 font=("Arial", 14), bg="#eef7ff", fg="red").pack(pady=10)
    else:
        for alimento in resultado:
            texto = f"• {alimento['nombre']} → {alimento['beneficio']}"
            tk.Label(frame, text=texto, font=("Arial", 12),
                     bg="#eef7ff", justify="left").pack(anchor="w", padx=20)

    tk.Button(frame, text="Regresar al menú",
              font=("Arial", 12, "bold"), bg="#2b7cc3", fg="white",
              command=mostrar_menu).pack(pady=20)

    tk.Button(frame, text="Salir",
              font=("Arial", 12, "bold"), bg="#d9534f", fg="white",
              command=ventana.quit).pack(pady=5)

# ------------------------------------------
# LIMPIAR PANTALLA
# ------------------------------------------
def limpiar_pantalla():
    for widget in frame.winfo_children():
        widget.destroy()

# ------------------------------------------
# VENTANA PRINCIPAL
# ------------------------------------------
ventana = tk.Tk()
ventana.title("Nutri - Tu Doctor de Confianza")
ventana.geometry("550x700")
ventana.configure(bg="#eef7ff")
ventana.resizable(False, False)

frame = tk.Frame(ventana, bg="#eef7ff")
frame.pack(fill="both", expand=True)

# Iniciar pidiendo datos
pedir_datos_usuario()

ventana.mainloop()
