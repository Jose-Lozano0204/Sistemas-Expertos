import numpy as np
import matplotlib.pyplot as plt

# Lozano Hernandez Jose Angel  22310220 7F

# Datos: horas de estudio (x) y calificación real (y)
x = np.array([1, 2, 3, 4, 5])         # horas de estudio por semana
y = np.array([2, 4, 6, 8, 10])        # calificación esperada (ejemplo y = 2x)

# Peso inicial (supongamos que el maestro cree que w1 = 3)
w1 = 3

# Calcular predicciones y error con ese peso
y_estimada = w1 * x
E = (1 / (2 * len(x))) * np.sum(np.power(y - y_estimada, 2))

# Rango de valores posibles para w1
w1_values = np.linspace(0, 5, 50)
E_values = []

# Calcular el error para cada posible w1
for w in w1_values:
    y_es = w * x
    E_temp = (1 / (2 * len(x))) * np.sum(np.power(y - y_es, 2))
    E_values.append(E_temp)

# Graficar curva de error
plt.figure(figsize=(8, 5))
plt.plot(w1_values, E_values, label="Error medio E", color="red")

# Punto específico para w1 elegido
plt.scatter(w1, E, color="blue", zorder=3, label=f"Punto ($w_1={w1}$, $E={E:.2f}$)")

# Configuración
plt.xlabel("$w_1$ (peso: horas → calificación)")
plt.ylabel("Error $E$")
plt.title("Error al predecir calificaciones en función de $w_1$")
plt.legend()
plt.grid()
plt.show()

# Mostrar el error
print(f"Si suponemos que cada hora de estudio suma {w1} puntos a la calificación, el error medio es: {E:.4f}")
