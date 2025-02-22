import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean, median, stdev, mode
import io
import base64

# =========================
# 1. Datos y Ordenamiento
# =========================
data = [
199.2, 199.7, 201.8, 202.0, 201.0, 201.5, 200.0, 199.8,
    200.7, 201.4, 200.4, 201.7, 201.4, 201.4, 200.8, 202.1,
    200.7, 200.9, 201.0, 201.5, 201.2, 201.3, 200.9, 200.7,
    200.5, 201.2, 201.7, 201.2, 200.5, 201.1, 201.4, 201.4,
    200.2, 201.0, 201.4, 201.4, 201.1, 201.2, 201.0, 200.6,
    202.0, 201.0, 201.5, 201.6, 200.6, 200.1, 201.3, 200.6,
    200.7, 201.8, 200.5, 200.5, 200.8, 200.3, 200.7, 199.5,
    198.6, 200.3, 198.5, 198.2, 199.6, 198.4, 199.0, 199.0,
    199.7, 199.7, 199.0, 198.4, 199.1, 198.8, 198.3, 198.9,
    199.6, 199.0, 198.7, 200.5, 198.4, 198.8, 198.5, 198.5,
    198.9, 198.8, 198.7, 199.2, 199.3, 197.8, 199.9, 198.9,
    199.0, 199.0, 198.7, 199.1, 200.3, 200.5, 198.1, 198.3,
    199.6, 199.0, 199.7, 198.9, 199.2, 197.9, 200.3, 199.6,
    199.4, 198.7, 198.5, 198.7, 198.6, 198.5
]
data.sort()
n = len(data)

# =========================
# 2. Medidas Estadísticas Básicas
# =========================
media = mean(data)
mediana = median(data)
try:
    mod = mode(data)
except:
    mod = np.nan  # En caso de múltiples modas o no definida

desv_est = stdev(data)  # Desviación estándar muestral
varianza = desv_est**2
CV = (desv_est / media) * 100
Xmin, Xmax = min(data), max(data)
R = Xmax - Xmin

# Cuartiles (Q1, Q2=Mediana, Q3)
q1, q2, q3 = np.percentile(data, [25, 50, 75])

# =========================
# 3. Intervalos de Clase (Sturges)
# =========================
K = math.ceil(1 + 3.3 * math.log10(n))  # Redondeo hacia arriba
ancho_clase = R / K

clases_lim_inf = []
clases_lim_sup = []
lim_inferior = Xmin
for i in range(K):
    lim_superior = lim_inferior + ancho_clase
    clases_lim_inf.append(lim_inferior)
    clases_lim_sup.append(lim_superior)
    lim_inferior = lim_superior

# =========================
# 4. Tabla de Frecuencias
# =========================
frecuencias = []
for i in range(K):
    lim_inf = clases_lim_inf[i]
    lim_sup = clases_lim_sup[i]
    if i < K - 1:
        count = sum(1 for x in data if lim_inf <= x < lim_sup)
    else:
        count = sum(1 for x in data if lim_inf <= x <= lim_sup)
    frecuencias.append(count)

frecuencia_acumulada = np.cumsum(frecuencias)
frecuencia_porcentual = [(f / n) * 100 for f in frecuencias]
frecuencia_porcentual_acumulada = np.cumsum(frecuencia_porcentual)
marcas_clase = [(clases_lim_inf[i] + clases_lim_sup[i]) / 2 for i in range(K)]

tabla_frecuencia = pd.DataFrame({
    "Clase": range(1, K+1),
    "Límite Inferior": clases_lim_inf,
    "Límite Superior": clases_lim_sup,
    "Marca de Clase": marcas_clase,
    "Frecuencia Absoluta": frecuencias,
    "Frecuencia Acumulada": frecuencia_acumulada,
    "Frecuencia %": frecuencia_porcentual,
    "Frecuencia % Acumulada": frecuencia_porcentual_acumulada
})

# =========================
# 5. Coeficiente de Asimetría (Pearson)
# =========================
if not np.isnan(mod):
    As = (media - mod) / desv_est
else:
    As = (3 * (media - mediana)) / desv_est

if As > 0:
    sesgo = "Sesgada a la derecha (positiva)"
elif As < 0:
    sesgo = "Sesgada a la izquierda (negativa)"
else:
    sesgo = "Distribución simétrica"

# =========================
# 6. Regla Empírica (intervalos ±1σ, ±2σ, ±3σ)
# =========================
emp_68_inf = media - desv_est
emp_68_sup = media + desv_est
emp_95_inf = media - 2 * desv_est
emp_95_sup = media + 2 * desv_est
emp_99_inf = media - 3 * desv_est
emp_99_sup = media + 3 * desv_est

# =========================
# 7. Tabla Resumen (Medidas de Dispersión, Cuartiles, etc.)
# =========================
tabla_dispersion = pd.DataFrame({
    "Medida": [
        "Rango",
        "Varianza",
        "Desviación Estándar",
        "Coef. Variación (%)",
        "Asimetría (As)",
        "Q1 (25%)",
        "Mediana (Q2)",
        "Q3 (75%)"
    ],
    "Valor": [
        f"{R:.2f}",
        f"{varianza:.2f}",
        f"{desv_est:.2f}",
        f"{CV:.2f}",
        f"{As:.2f}",
        f"{q1:.2f}",
        f"{q2:.2f}",
        f"{q3:.2f}"
    ],
    "Intervalo 68% (±1σ)": [
        f"{emp_68_inf:.2f} a {emp_68_sup:.2f}", "", "", "", "", "", "", ""
    ],
    "Intervalo 95% (±2σ)": [
        f"{emp_95_inf:.2f} a {emp_95_sup:.2f}", "", "", "", "", "", "", ""
    ],
    "Intervalo 99.7% (±3σ)": [
        f"{emp_99_inf:.2f} a {emp_99_sup:.2f}", "", "", "", "", "", "", ""
    ]
})

# =========================
# 8. Función para convertir gráficos a Base64
# =========================
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_base64

# Título de la variable principal
variable_principal = "En (mm)"

# Histograma
fig_hist, ax_hist = plt.subplots(figsize=(8, 4))
ax_hist.hist(data, bins=clases_lim_sup, edgecolor='black', alpha=0.7)
ax_hist.set_title("Histograma de Frecuencias")
ax_hist.set_xlabel("Clases (" + variable_principal + ")")
ax_hist.set_ylabel("Frecuencia Absoluta")
ax_hist.grid(axis='y', linestyle='--', alpha=0.7)
img_hist = fig_to_base64(fig_hist)

# Boxplot
fig_box, ax_box = plt.subplots(figsize=(4, 6))
ax_box.boxplot(data, vert=True, patch_artist=True)
ax_box.set_title("Diagrama de Caja (Boxplot)")
ax_box.set_ylabel(variable_principal)
ax_box.grid(axis='y', linestyle='--', alpha=0.7)
img_box = fig_to_base64(fig_box)

# =========================
# 9. Clasificación en Cuartiles, Deciles y Percentiles
# =========================
# Para cada observación, se calcula el percentil (usando ranking) y se asigna:
# - Cuartil: según los límites Q1, Q2, Q3.
# - Decil: usando el percentil, se asigna la decil = ceil(percentil/10)
clasificacion = []
for x in data:
    # Cálculo del ranking para el percentil
    count_menores = sum(1 for v in data if v < x)
    count_iguales = sum(1 for v in data if v == x)
    rank = count_menores + 0.5 * count_iguales
    perc = (rank / n) * 100

    # Asignar cuartil basado en los valores de Q1, Q2 y Q3
    if x <= q1:
        cuartil = 1
    elif x <= q2:
        cuartil = 2
    elif x <= q3:
        cuartil = 3
    else:
        cuartil = 4

    # Asignar decil: se divide el percentil en 10 grupos
    decil = math.ceil(perc / 10) if perc > 0 else 1

    clasificacion.append((x, cuartil, decil, perc))

tabla_clasificacion = pd.DataFrame(clasificacion, columns=["Valor", "Cuartil", "Decil", "Percentil (%)"])

# =========================
# 10. Generación de la Página HTML con la paleta
# =========================
html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Análisis Estadístico Descriptivo</title>
    <style>
        /* Paleta de colores
           STORMY:   #494E6B
           CLOUD:    #98878F
           SUNSET:   #985E6D
           EVENING:  #192231
        */

        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #192231; /* EVENING */
            color: #e5e8e8; /* Texto claro */
        }}

        h1 {{
            color: #985E6D; /* SUNSET */
            margin-bottom: 0.5em;
        }}

        h2 {{
            color: #494E6B; /* STORMY */
            margin-top: 1.2em;
        }}

        ul {{
            list-style-type: none; 
            padding: 0;
        }}
        ul li {{
            margin: 5px 0;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
            color: #e5e8e8; /* Texto de tabla */
        }}

        table, th, td {{
            border: 1px solid #98878F; /* CLOUD */
        }}

        th {{
            background-color: #494E6B; /* STORMY */
            color: #e5e8e8;
            padding: 8px;
            text-align: center;
        }}

        td {{
            padding: 8px;
            text-align: center;
            background-color: rgba(255, 255, 255, 0.04); /* Leve contraste */
        }}

        .grafico {{
            margin-bottom: 30px;
        }}

        .tabla-resumen td:nth-child(1) {{
            text-align: left;
        }}

        /* Encabezados de la tabla de resumen */
        .tabla-resumen thead th {{
            background-color: #494E6B; /* STORMY */
            color: #e5e8e8;
        }}

        /* Hover en filas de tabla */
        tr:hover {{
            background-color: rgba(152, 135, 143, 0.15); /* CLOUD con transparencia */
        }}

        img {{
            border: 2px solid #98878F; /* CLOUD */
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <h1>Análisis Estadístico Descriptivo</h1>

    <h2>Estadísticas Básicas</h2>
    <ul>
        <li>Total de datos (n): {n}</li>
        <li>Valor mínimo (Xmin): {Xmin}</li>
        <li>Valor máximo (Xmax): {Xmax}</li>
        <li>Rango (R): {R:.2f}</li>
        <li>Número de clases (K): {K}</li>
        <li>Ancho de clase (w): {ancho_clase:.3f}</li>
        <li>Media (X̄): {media:.3f}</li>
        <li>Mediana (Me): {mediana:.3f}</li>
        <li>Moda (Mo): {"No definida" if np.isnan(mod) else f"{mod}"}</li>
        <li>Varianza (s²): {varianza:.4f}</li>
        <li>Desviación Estándar (s): {desv_est:.4f}</li>
        <li>Coef. de Variación (CV): {CV:.2f}%</li>
    </ul>

    <h2>Coeficiente de Asimetría</h2>
    <ul>
        <li>As: {As:.3f}</li>
        <li>Interpretación: {sesgo}</li>
    </ul>

    <h2>Tabla de Frecuencias</h2>
    {tabla_frecuencia.to_html(index=False, float_format="%.2f")}

    <h2>Medidas de Dispersión y Regla Empírica</h2>
    {tabla_dispersion.to_html(index=False, classes="tabla-resumen")}

    <div class="grafico">
        <h2>Histograma de Frecuencias</h2>
        <img src="data:image/png;base64,{img_hist}" alt="Histograma">
    </div>

    <div class="grafico">
        <h2>Diagrama de Caja (Boxplot)</h2>
        <img src="data:image/png;base64,{img_box}" alt="Boxplot">
    </div>

    <h2>Clasificación: Cuartiles, Deciles y Percentiles</h2>
    {tabla_clasificacion.to_html(index=False, float_format="%.2f")}

</body>
</html>
"""

# =========================
# 11. Guardar el HTML
# =========================
with open("resultado.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("El análisis se ha generado en 'resultado.html'. ¡Ábrelo en tu navegador para ver los resultados!")
