import numpy as np

# Lozano Hernandez Jose Angel 22310220 7F

# Características de frutas
# [tamaño, color, textura]
X = np.array([
    [1, 1, 1],   # Manzana grande, roja, lisa
    [-1, 1, 1],  # Manzana pequeña, roja, lisa
    [1, -1, -1], # Naranja grande, naranja, rugosa
    [-1, -1, -1] # Naranja pequeña, naranja, rugosa
])

# Etiquetas: 1 = manzana, -1 = naranja
y_true = np.array([1, 1, -1, -1])

# Pesos iniciales
w = np.array([0.5, 0.5, 0.5])

# Tasa de aprendizaje
learning_rate = 0.5

# Numero maximo de epocas
max_epochs = 10

def train_perceptron(X, y_true, w, learning_rate, max_epochs=10):
    for epoch in range(max_epochs):
        errors = 0
        for i in range(len(X)):
            x = X[i, :]
            y = y_true[i]
            z = np.dot(w, x)
            y_pred = np.sign(z)
            if y_pred == 0:
                y_pred = 1
            if y_pred != y:
                w += learning_rate * (y - y_pred) * x
                errors += 1
        print(f"Epoca {epoch+1}, Errores: {errors}")
        if errors == 0:
            print("¡Modelo aprendido correctamente!")
            break
    return w

# Entrenar perceptron
w_final = train_perceptron(X, y_true, w, learning_rate, max_epochs)

# Probar el modelo
print("\n--- Predicciones ---")
for i in range(len(X)):
    x = X[i, :]
    z = np.dot(w_final, x)
    y_pred = np.sign(z)
    if y_pred == 0:
        y_pred = 1
    fruta = "Manzana" if y_pred == 1 else "Naranja"
    print(f"Entrada {x} -> Prediccion: {fruta}")

