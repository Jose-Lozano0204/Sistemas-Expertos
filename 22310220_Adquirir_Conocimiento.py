import json
import os

# Archivo donde guardaremos el conocimiento aprendido
DB_FILE = "conocimiento.json"

# Base de conocimiento inicial
base_conocimiento = {
    "hola": "¡Hola! ¿Cómo estás?",
    "como estas": "Estoy bien, gracias por preguntar. ¿Y tú?",
    "de que te gustaria hablar": "Podemos hablar de programación, ciencia o lo que quieras."
}

# Cargar conocimiento previo si existe
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        base_conocimiento.update(json.load(f))


def guardar_conocimiento():
    """Guarda la base de conocimiento en un archivo JSON."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(base_conocimiento, f, indent=4, ensure_ascii=False)


print("=== ChatBot con Aprendizaje ===")
print("Escribe 'salir' para terminar.\n")

while True:
    usuario = input("Tú: ").lower().strip()

    if usuario == "salir":
        print("ChatBot: ¡Adios! Hasta la proxima ")
        guardar_conocimiento()
        break

    # Buscar respuesta
    if usuario in base_conocimiento:
        print("ChatBot:", base_conocimiento[usuario])
    else:
        print("ChatBot: No se que responder a eso ")
        nueva_respuesta = input("¿Que deberia responder cuando me digan eso?: ").strip()

        if nueva_respuesta:
            base_conocimiento[usuario] = nueva_respuesta
            guardar_conocimiento()
            print("ChatBot: ¡Gracias! Aprendi algo nuevo ")
