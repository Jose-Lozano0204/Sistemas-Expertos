import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import textwrap

# ------------------------------------------------------------------
# Datos
# ------------------------------------------------------------------
personajes = {
    "Edgar (Cazador)": "imagenes/edgar.png",
    "Helga (Cazadora)": "imagenes/helga.png",
    "Morgana (Bruja)": "imagenes/morgana.png",
    "Salem (Brujo)": "imagenes/salem.jpg",
    "Lilith (Bruja)": "imagenes/lilith.png"
}

armas = {
    "Varita maldita": "imagenes/varita.png",
    "Cetro de fuego": "imagenes/cetro.jpg",
    "Daga encantada": "imagenes/daga.jpg",
    "Poción venenosa": "imagenes/pocion.png",
    "Libro de hechizos prohibido": "imagenes/libro.jpg"
}

# ------------------------------------------------------------------
# Escenas narrativas
# ------------------------------------------------------------------
escenas = [
    {
        "culpable": "Edgar (Cazador)",
        "victima": "Morgana (Bruja)",
        "arma": "Poción venenosa",
        "fondo": "imagenes/cocina.jpg",
        "texto": (
            "Una tormenta azota la mansión. Las luces se apagan y las figuras se dispersan.\n"
            "Entre frascos rotos y el aroma a pociones, algo terrible sucede. Un grito resuena."
        )
    },
    {
        "culpable": "Salem (Brujo)",
        "victima": "Helga (Cazadora)",
        "arma": "Cetro de fuego",
        "fondo": "imagenes/biblioteca.jpg",
        "texto": (
            "La biblioteca secreta está iluminada solo por unas velas que parpadean.\n"
            "Un estallido de fuego sorprende a uno de los presentes."
        )
    },
    {
        "culpable": "Lilith (Bruja)",
        "victima": "Salem (Brujo)",
        "arma": "Libro de hechizos prohibido",
        "fondo": "imagenes/mansion.jpg",
        "texto": (
            "En la gran sala, se corta la luz y un hechizo antiguo golpea a alguien.\n"
            "Observa con atención la escena."
        )
    },
    {
        "culpable": "Morgana (Bruja)",
        "victima": "Lilith (Bruja)",
        "arma": "Daga encantada",
        "fondo": "imagenes/cripta.jpeg",
        "texto": (
            "La cripta subterránea está envuelta en niebla.\n"
            "Se escuchan murmullos y cadenas arrastrándose, y un enfrentamiento mortal ocurre."
        )
    },
    {
        "culpable": "Helga (Cazadora)",
        "victima": "Edgar (Cazador)",
        "arma": "Varita maldita",
        "fondo": "imagenes/bosque.jpg",
        "texto": (
            "El bosque oscuro envuelve a los presentes.\n"
            "Un grito rompe la calma y la niebla oculta los movimientos del culpable."
        )
    }
]

# ------------------------------------------------------------------
# Estado del juego
# ------------------------------------------------------------------
final_escena = None
seleccion_culpable = None
seleccion_victima = None
seleccion_arma = None
intentos = 5
pistas_dadas = 0
_loaded_images = {}

# ------------------------------------------------------------------
# Funciones auxiliares
# ------------------------------------------------------------------
def cargar_imagen(path, size):
    key = (path, size)
    if key in _loaded_images:
        return _loaded_images[key]
    img = Image.open(path).convert("RGBA").resize(size, Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    _loaded_images[key] = tk_img
    return tk_img

# ------------------------------------------------------------------
# Funciones del juego
# ------------------------------------------------------------------
def iniciar_partida():
    global final_escena, seleccion_culpable, seleccion_victima, seleccion_arma, intentos, pistas_dadas
    final_escena = random.choice(escenas)
    seleccion_culpable = seleccion_victima = seleccion_arma = None
    intentos = 5
    pistas_dadas = 0
    menu_frame.pack_forget()
    mostrar_escena_frame(final_escena)

def reiniciar_a_menu():
    escena_frame.pack_forget()
    deduccion_frame.pack_forget()
    resultado_frame.pack_forget()
    menu_frame.pack(expand=True)

def mostrar_escena_frame(escena):
    # Limpiar escena
    for widget in escena_frame.winfo_children():
        widget.destroy()
    escena_frame.pack(fill="both", expand=True)

    fondo_img = cargar_imagen(escena["fondo"], (920, 450))
    fondo_label = tk.Label(escena_frame, image=fondo_img)
    fondo_label.image = fondo_img
    fondo_label.pack()

    narr_label = tk.Label(escena_frame, text="\n".join(textwrap.wrap(escena["texto"], 100)),
                          font=("Arial",12), wraplength=850, justify="left")
    narr_label.pack(pady=10)

    tk.Button(escena_frame, text="Deducir culpable", command=ir_a_deduccion).pack(pady=10)
    tk.Button(escena_frame, text="Volver al menú", command=reiniciar_a_menu).pack(pady=5)

def ir_a_deduccion():
    escena_frame.pack_forget()
    preparar_pantalla_deduccion()
    deduccion_frame.pack(fill="both", expand=True)

def preparar_pantalla_deduccion():
    for cont in [culpables_container, victimas_container, armas_container]:
        for w in cont.winfo_children():
            w.destroy()

    # Víctimas
    tk.Label(victimas_container, text="Selecciona la víctima", font=("Arial",12)).pack()
    for nombre, ruta in personajes.items():
        frame = tk.Frame(victimas_container, bd=2)
        frame.pack(side="left", padx=5)
        img = cargar_imagen(ruta, (90,90))
        lbl = tk.Label(frame, image=img)
        lbl.image = img
        lbl.pack()
        lbl.bind("<Button-1>", lambda e, n=nombre, f=frame: seleccionar_victima(n,f))

    # Culpables
    tk.Label(culpables_container, text="Selecciona el culpable", font=("Arial",12)).pack()
    for nombre, ruta in personajes.items():
        frame = tk.Frame(culpables_container, bd=2)
        frame.pack(side="left", padx=5)
        img = cargar_imagen(ruta, (90,90))
        lbl = tk.Label(frame, image=img)
        lbl.image = img
        lbl.pack()
        lbl.bind("<Button-1>", lambda e, n=nombre, f=frame: seleccionar_culpable(n,f))

    # Armas
    tk.Label(armas_container, text="Selecciona el arma", font=("Arial",12)).pack()
    for nombre, ruta in armas.items():
        frame = tk.Frame(armas_container, bd=2)
        frame.pack(side="left", padx=5)
        img = cargar_imagen(ruta, (80,80))
        lbl = tk.Label(frame, image=img)
        lbl.image = img
        lbl.pack()
        lbl.bind("<Button-1>", lambda e, n=nombre, f=frame: seleccionar_arma(n,f))

    # Limpiar botón anterior
    for w in deduccion_frame.pack_slaves():
        if isinstance(w, tk.Button) and w.cget("text") == "Verificar deducción":
            w.destroy()

    global boton_verificar_deduccion
    boton_verificar_deduccion = tk.Button(deduccion_frame, text="Verificar deducción",
                                          state="disabled", command=verificar_deduccion)
    boton_verificar_deduccion.pack(pady=10)

def marcar_seleccion(container, frame):
    for child in container.winfo_children():
        child.config(relief="flat")
    frame.config(relief="solid", bd=3)

def seleccionar_victima(n, f):
    global seleccion_victima
    seleccion_victima = n
    marcar_seleccion(victimas_container, f)
    actualizar_boton_verificar()

def seleccionar_culpable(n, f):
    global seleccion_culpable
    seleccion_culpable = n
    marcar_seleccion(culpables_container, f)
    actualizar_boton_verificar()

def seleccionar_arma(n, f):
    global seleccion_arma
    seleccion_arma = n
    marcar_seleccion(armas_container, f)
    actualizar_boton_verificar()

def actualizar_boton_verificar():
    if seleccion_victima and seleccion_culpable and seleccion_arma:
        boton_verificar_deduccion.config(state="normal")
    else:
        boton_verificar_deduccion.config(state="disabled")

def verificar_deduccion():
    global intentos, pistas_dadas
    if (seleccion_victima == final_escena["victima"] and
        seleccion_culpable == final_escena["culpable"] and
        seleccion_arma == final_escena["arma"]):
        deduccion_frame.pack_forget()
        resultado_label.config(text="¡Correcto! Has resuelto la escena.\n\n" + final_escena["texto"] +
                              f"\n\nRespuesta:\nVíctima: {final_escena['victima']}\nCulpable: {final_escena['culpable']}\nArma: {final_escena['arma']}")
        resultado_frame.pack(fill="both", expand=True)
    else:
        intentos -= 1
        pistas_dadas += 1
        if intentos > 0:
            messagebox.showwarning(
                "Incorrecto",
                f"No es la combinación correcta.\nTe quedan {intentos} intento(s).\n\nPista:\n{generar_pista(pistas_dadas)}"
            )
        else:
            messagebox.showerror(
                "Game Over",
                f"Has agotado tus intentos.\nLa víctima era {final_escena['victima']}, "
                f"el culpable era {final_escena['culpable']} con {final_escena['arma']}."
            )
            reiniciar_a_menu()

def generar_pista(n):
    if n == 1:
        # Primer pista: tipo del culpable
        tipo = final_escena['culpable'].split("(")[1][:-1]  # Cazador/Brujo/Bruja
        return f"El culpable es un {tipo}."
    elif n == 2:
        # Segundo pista: tipo de arma
        arma = final_escena['arma']
        if "Varita" in arma or "Cetro" in arma or "Libro" in arma:
            return "El arma utilizada tiene magia oscura."
        else:
            return "El arma utilizada es física y mortal."
    elif n == 3:
        # Pista de observación
        return "Observa los detalles de la escena: expresiones, gestos y objetos cercanos."
    elif n == 4:
        # Diferenciación de víctima
        tipo_victima = final_escena['victima'].split("(")[1][:-1]
        return f"La víctima era un(a) {tipo_victima}."
    else:
        return "Última oportunidad: usa toda tu deducción para adivinar correctamente."

# ------------------------------------------------------------------
# INTERFAZ
# ------------------------------------------------------------------
ventana = tk.Tk()
ventana.title("Clue - Cazador de Brujas")
ventana.geometry("920x780")

# --- MENÚ ---
menu_frame = tk.Frame(ventana, width=920, height=780)
menu_frame.pack_propagate(False)
menu_frame.pack(expand=True)

fondo_menu_img = Image.open("imagenes/fondo.jpeg").resize((920,780))
fondo_menu_tk = ImageTk.PhotoImage(fondo_menu_img)
fondo_label_menu = tk.Label(menu_frame, image=fondo_menu_tk)
fondo_label_menu.place(x=0, y=0, relwidth=1, relheight=1)

tk.Label(menu_frame, text="Clue: Cazador vs Brujas", font=("Arial",20), fg="white", bg="black").place(relx=0.5, rely=0.2, anchor="center")
tk.Button(menu_frame, text="JUGAR", font=("Arial",14), command=iniciar_partida, bg="white").place(relx=0.5, rely=0.5, anchor="center")
tk.Button(menu_frame, text="SALIR", font=("Arial",14), command=ventana.destroy, bg="white").place(relx=0.5, rely=0.6, anchor="center")
tk.Label(menu_frame, text="Observa la escena y luego deduce la víctima, el culpable y el arma.", fg="white", bg="black", justify="center", wraplength=700).place(relx=0.5, rely=0.75, anchor="center")

# --- ESCENA ---
escena_frame = tk.Frame(ventana)

# --- DEDUCCIÓN ---
deduccion_frame = tk.Frame(ventana)
victimas_container = tk.Frame(deduccion_frame)
victimas_container.pack(pady=5)
culpables_container = tk.Frame(deduccion_frame)
culpables_container.pack(pady=5)
armas_container = tk.Frame(deduccion_frame)
armas_container.pack(pady=5)
boton_verificar_deduccion = tk.Button(deduccion_frame, text="Verificar deducción", state="disabled", command=verificar_deduccion)
boton_verificar_deduccion.pack(pady=10)

# --- RESULTADO ---
resultado_frame = tk.Frame(ventana)
resultado_label = tk.Label(resultado_frame, text="", wraplength=850, justify="left", font=("Arial",12))
resultado_label.pack(pady=20)
tk.Button(resultado_frame, text="Jugar de nuevo", command=lambda: [resultado_frame.pack_forget(), iniciar_partida()]).pack(pady=6)
tk.Button(resultado_frame, text="Volver al menú", command=reiniciar_a_menu).pack(pady=6)

ventana.mainloop()
