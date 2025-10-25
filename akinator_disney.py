import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import json
import os

DB_FILE = "disney.json"

# ---------------- Funciones de Base de Datos ----------------
def cargar_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4, ensure_ascii=False)

# ---------------- Clase Juego ----------------
class JuegoAkinator:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator Disney")
        self.root.geometry("400x450")
        self.root.configure(bg="#ADD8E6")  # Fondo azul bajito

        self.db = cargar_db()
        if not self.db:
            messagebox.showerror("Error", "Base de datos vacía. Asegúrate de tener el archivo disney.json.")
            self.root.quit()

        self.mostrar_menu_principal()

    # -------- Menú Principal --------
    def mostrar_menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#ADD8E6")  # Fondo azul bajito

        titulo = tk.Label(self.root, text="🎩 Akinator Disney 🎩", font=("Arial", 18, "bold"), bg="#ADD8E6")
        titulo.pack(pady=40)

        jugar_btn = tk.Button(self.root, text="Jugar", width=20, height=2, command=self.iniciar_juego, bg="#87CEEB", fg="black")
        jugar_btn.pack(pady=10)

        salir_btn = tk.Button(self.root, text="Salir", width=20, height=2, command=self.root.quit, bg="#87CEEB", fg="black")
        salir_btn.pack(pady=10)

    # -------- Iniciar Juego --------
    def iniciar_juego(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#ADD8E6")  # Fondo azul bajito

        self.preguntas = [
            "es_un_villano", "es_una_princesa", "es_un_heroe",
            "es_un_animal", "es_humano", "es_un_juguete",
            "vuela", "tiene_orejas_grandes", "es_un_carro", "es_hombre",
            "su_vestido_es_azul", "su_vestido_es_amarillo", "es_una_sirena"
        ]
        self.pregunta_index = 0
        self.candidatos = self.db.copy()

        # Imagen del juego
        try:
            self.imagen = Image.open("imagen.jpg")  # Cambia aquí si tienes otra imagen
            self.imagen = self.imagen.resize((200, 200))
            self.imagen_tk = ImageTk.PhotoImage(self.imagen)
            self.imagen_label = tk.Label(self.root, image=self.imagen_tk, bg="#ADD8E6")
            self.imagen_label.pack(pady=10)
        except Exception:
            self.imagen_label = tk.Label(self.root, text="(No se pudo cargar la imagen)", bg="#ADD8E6")
            self.imagen_label.pack(pady=10)

        # Pregunta
        self.pregunta_label = tk.Label(self.root, text="¡Piensa en un personaje de Disney!", font=("Arial", 12), bg="#ADD8E6")
        self.pregunta_label.pack(pady=20)

        # Botones de respuesta
        self.si_button = tk.Button(self.root, text="Sí", width=20, command=lambda: self.responder("si"), bg="#87CEEB", fg="black")
        self.si_button.pack(pady=5)

        self.no_button = tk.Button(self.root, text="No", width=20, command=lambda: self.responder("no"), bg="#87CEEB", fg="black")
        self.no_button.pack(pady=5)

        # Botón para volver al menú
        self.regresar_btn = tk.Button(self.root, text="Volver al Menú", width=20, command=self.mostrar_menu_principal, bg="#87CEEB", fg="black")
        self.regresar_btn.pack(pady=15)

        self.siguiente_pregunta()

    # -------- Siguiente Pregunta --------
    def siguiente_pregunta(self):
        if self.pregunta_index >= len(self.preguntas):
            self.mostrar_resultado_final()
            return
        pregunta = self.preguntas[self.pregunta_index]
        self.pregunta_label.config(text=f"¿Tu personaje {pregunta.replace('_', ' ')}?")

    # -------- Responder --------
    def responder(self, respuesta):
        pregunta = self.preguntas[self.pregunta_index]

        # Filtrar candidatos según la respuesta
        self.candidatos = {
            nombre: datos
            for nombre, datos in self.candidatos.items()
            if datos.get(pregunta) == respuesta
        }

        if len(self.candidatos) == 1:
            self.personaje_encontrado = next(iter(self.candidatos))
            self.mostrar_resultado()
        elif len(self.candidatos) == 0:
            self.mostrar_no_conozco()
        else:
            self.pregunta_index += 1
            self.siguiente_pregunta()

    # -------- Resultado Encontrado --------
    def mostrar_resultado(self):
        personaje = self.personaje_encontrado
        if messagebox.askyesno("Resultado", f"¡Creo que tu personaje es... {personaje}!\n¿Adiviné correctamente?"):
            messagebox.showinfo("Éxito", "¡Sabía que lo lograría!")
            self.mostrar_menu_principal()
        else:
            self.mostrar_no_conozco()

    # -------- No Conozco --------
    def mostrar_no_conozco(self):
        if messagebox.askyesno("No lo conozco", "No conozco a ese personaje. ¿Quieres agregarlo a la base de datos?"):
            self.agregar_personaje()
        else:
            self.mostrar_menu_principal()

    # -------- Agregar Personaje --------
    def agregar_personaje(self):
        nuevo = simpledialog.askstring("Agregar personaje", "¿Cuál era tu personaje?")
        if not nuevo:
            self.mostrar_menu_principal()
            return

        nuevo_datos = {}
        for pregunta in self.preguntas:
            r = messagebox.askyesno("Pregunta", f"¿{nuevo} {pregunta.replace('_', ' ')}?")
            nuevo_datos[pregunta] = "si" if r else "no"

        self.db[nuevo] = nuevo_datos
        guardar_db(self.db)
        messagebox.showinfo("Agregado", f"{nuevo} agregado a la base de datos.")
        self.mostrar_menu_principal()

    # -------- Resultado final si no quedan preguntas --------
    def mostrar_resultado_final(self):
        if len(self.candidatos) == 1:
            self.personaje_encontrado = next(iter(self.candidatos))
            self.mostrar_resultado()
        elif len(self.candidatos) > 1:
            lista = "\n".join(self.candidatos.keys())
            messagebox.showinfo("Resultado", f"No pude adivinar con certeza. Podría ser uno de estos:\n{lista}")
            self.mostrar_menu_principal()
        else:
            self.mostrar_no_conozco()

# ---------------- Main ----------------
def main():
    root = tk.Tk()
    app = JuegoAkinator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
