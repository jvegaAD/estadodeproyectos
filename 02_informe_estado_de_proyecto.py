import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Ruta del archivo Excel
file_path = r"PQ_Espejo_Datos_Macro.xlsx"

# Cargar el archivo Excel
df = pd.read_excel(file_path, sheet_name='PQ_Espejo_Datos_Macro')

# ----- Parte 1: Visualización de la información filtrada -----

# Filtrar las filas donde 'Clasificación Capítulo (Texto12)' es igual a 'Partida'
df_filtrado = df[df['Clasificación Capítulo (Texto12)'] == 'Partida']

# Seleccionar las columnas especificadas del DataFrame filtrado
df_seleccion = df_filtrado[['Id', 'Clasificación Capítulo (Texto12)', 'Tema', 'Responsable', 'Nombre de tarea', '% Completado Real Hoy', 'Diferencia Avance']]

# Título de la aplicación con fontsize=10 y fontweight='bold'
st.markdown("<h1 style='font-size:20pt; font-weight:bold;'>Visualización de la Información de avance del Proyecto</h1>", unsafe_allow_html=True)

# Texto "Tabla de Resumen:" con fontsize=10 y fontweight='bold'
st.markdown("<h2 style='font-size:15pt; font-weight:bold;'>Tabla de Resumen:</h2>", unsafe_allow_html=True)

# Mostrar el DataFrame filtrado en Streamlit
st.dataframe(df_seleccion)

# ----- Parte 2: Gráfico de Avance por Responsable -----

# Agrupar por 'Responsable' y calcular los promedios de '% Completado Programado', '% Completado Real Hoy' y 'Diferencia Avance'
df_grouped = df_filtrado[['Responsable', '% Completado Programado', '% Completado Real Hoy', 'Diferencia Avance']].groupby('Responsable').mean().reset_index()

# Tamaño del gráfico
fig, ax = plt.subplots(figsize=(10, 6))

# Índice de los responsables
responsables = df_grouped['Responsable']
y_pos = np.arange(len(responsables)) * 2  # Aumentar el espacio entre los responsables

# Ancho de las barras
bar_width = 0.4  # Ajustar el ancho de las barras para que sean más visibles con el espacio añadido

# Graficar las barras con espacio entre ellas
barras_programado = ax.barh(y_pos, df_grouped['% Completado Programado'], height=bar_width, color='dodgerblue', label='% Proyectado')
barras_real = ax.barh(y_pos + bar_width, df_grouped['% Completado Real Hoy'], height=bar_width, color='orange', label='% Real Hoy')
barras_diferencia = ax.barh(y_pos - bar_width, df_grouped['Diferencia Avance'], height=bar_width, color='red', label='Diferencia')

# Añadir etiquetas a las barras
for i in range(len(df_grouped)):
    ax.text(df_grouped['% Completado Programado'].iloc[i] + 0.5, y_pos[i], f"{int(df_grouped['% Completado Programado'].iloc[i])}%", color='black', va='center')
    ax.text(df_grouped['% Completado Real Hoy'].iloc[i] + 0.5, y_pos[i] + bar_width, f"{int(df_grouped['% Completado Real Hoy'].iloc[i])}%", color='black', va='center')
    ax.text(df_grouped['Diferencia Avance'].iloc[i] + 0.5, y_pos[i] - bar_width, f"{int(df_grouped['Diferencia Avance'].iloc[i])}%", color='black', va='center')

# Etiquetas y leyenda
ax.set_xlabel('AVANCE')
ax.set_ylabel('RESPONSABLES')
ax.set_yticks(y_pos)
ax.set_yticklabels(responsables)
ax.set_title('Gráfico de Avance por Responsable', fontsize=15, fontweight='bold')  # Título reducido y en negrita
ax.legend()

# Ajustar espaciado en el gráfico
plt.tight_layout()

# Mostrar gráfico en Streamlit
st.pyplot(fig)

# Estando la terminal ubicada en la carpeta del proyecto, Activar la aplicacion:   streamlit run 02_informe_estado_de_proyecto.py
