import numpy as np
import matplotlib.pyplot as plt
from    sklearn.linear_model import LinearRegression

def ingresar_datos():
    """Permite al usuario ingresar los datos de X y Y."""
    n = int(input("Ingrese la cantidad de datos: "))
    X = []
    Y = []
    for i in range(n):
        x = float(input(f"Ingrese X[{i+1}]: "))
        y = float(input(f"Ingrese Y[{i+1}]: "))
        X.append(x)
        Y.append(y)
    return np.array(X).reshape(-1, 1), np.array(Y)

def entrenar_modelo(X, Y):
    """Entrena un modelo de regresión lineal con los datos proporcionados."""
    modelo = LinearRegression()
    modelo.fit(X, Y)
    return modelo

def predecir(modelo):
    """Permite predecir valores de Y dada una X o viceversa."""
    while True:
        opcion = input("¿Desea predecir un valor de Y para una X dada? (s/n): ").strip().lower()
        if opcion == 's':
            x_nueva = float(input("Ingrese el valor de X para predecir Y: "))
            y_pred = modelo.predict(np.array([[x_nueva]]))[0]
            print(f"Predicción: Para X = {x_nueva}, Y estimado = {y_pred:.2f}")
        else:
            break

def graficar(X, Y, modelo):
    """Genera un gráfico con los datos y la regresión lineal."""
    plt.scatter(X, Y, color='blue', label='Datos reales')
    plt.plot(X, modelo.predict(X), color='red', label='Regresión lineal')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Regresión Lineal')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    print("Bienvenido a la herramienta de Regresión Lineal")
    X, Y = ingresar_datos()
    modelo = entrenar_modelo(X, Y)
    graficar(X, Y, modelo)
    predecir(modelo)

if __name__ == "__main__":
    main()
