import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, scrolledtext

# Cargar el dataset
df = pd.read_csv('diamonds.csv')

# Calcular estadísticas con Pandas y NumPy
media_precio = np.mean(df['price'])  # Media con NumPy
mediana_precio = np.median(df['price'])  # Mediana con NumPy
moda_precio = df['price'].value_counts().idxmax()  # Moda con Pandas

# Codificar la variable categórica 'cut' en valores numéricos
cut_mapping = {'Fair': 1, 'Good': 2, 'Very Good': 3, 'Premium': 4, 'Ideal': 5}
df['cut_numeric'] = df['cut'].map(cut_mapping)

# Calcular la varianza del precio por tipo de corte
varianza_precio_por_corte = df.groupby('cut')['price'].var()

# Crear la ventana principal
root = tk.Tk()
root.title("Análisis de Diamantes")
root.geometry("800x500")

# 📌 **Sección 1: Estadísticas del Precio (Texto)**
frame_stats = tk.Frame(root, padx=10, pady=10)
frame_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

label_stats = tk.Label(frame_stats, text="📊 Estadísticas del Precio de Diamantes 📊", font=("Arial", 14, "bold"))
label_stats.pack(pady=5)

texto = scrolledtext.ScrolledText(frame_stats, wrap=tk.WORD, font=("Arial", 12), width=40, height=5)
texto.pack()

info_texto = f"📌 Media: {media_precio:.2f}\n"
info_texto += f"📌 Mediana: {mediana_precio:.2f}\n"
info_texto += f"📌 Moda: {moda_precio}\n"

texto.insert(tk.END, info_texto)
texto.config(state=tk.DISABLED)  # Hacer el cuadro de texto solo lectura

# 📌 **Sección 2: Gráficos Interactivos**
frame_graphs = tk.Frame(root, padx=10, pady=10)
frame_graphs.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

label_graphs = tk.Label(frame_graphs, text="Seleccione un gráfico:", font=("Arial", 12))
label_graphs.pack(pady=5)

combo_graficos = ttk.Combobox(frame_graphs, values=[
    'Boxplot Corte vs Precio',
    'Violinplot Corte vs Precio',
    'Dispersión Corte (Codificado) vs Precio',
    'Boxplot Color vs Precio',
    'Varianza del Precio por Corte'
])
combo_graficos.pack(pady=5)
combo_graficos.current(0)


def mostrar_grafico():
    grafico = combo_graficos.get()
    plt.figure(figsize=(10, 6))

    if grafico == 'Boxplot Corte vs Precio':
        sns.boxplot(x='cut', y='price', data=df)
        plt.title('Relación entre el corte y el precio de los diamantes')
        plt.xlabel('Corte')
        plt.ylabel('Precio')

    elif grafico == 'Violinplot Corte vs Precio':
        sns.violinplot(x='cut', y='price', data=df)
        plt.title('Relación entre el corte y el precio de los diamantes')
        plt.xlabel('Corte')
        plt.ylabel('Precio')

    elif grafico == 'Dispersión Corte (Codificado) vs Precio':
        sns.scatterplot(x='cut_numeric', y='price', data=df, alpha=0.3)
        plt.xticks(ticks=range(1, 6), labels=cut_mapping.keys())
        plt.title('Dispersión entre el corte y el precio')
        plt.xlabel('Corte (Codificado)')
        plt.ylabel('Precio')

    elif grafico == 'Boxplot Color vs Precio':
        sns.boxplot(x='color', y='price', data=df)
        plt.title('Relación entre el color y el precio de los diamantes')
        plt.xlabel('Color')
        plt.ylabel('Precio')

    elif grafico == 'Varianza del Precio por Corte':
        sns.barplot(x=varianza_precio_por_corte.index,y=varianza_precio_por_corte.values,hue=varianza_precio_por_corte.index,palette='viridis',legend=False)
        plt.title('Varianza del Precio por Tipo de Corte')
        plt.xlabel('Corte')
        plt.ylabel('Varianza del Precio')

    plt.xticks(rotation=45)
    plt.show()


boton_mostrar = tk.Button(frame_graphs, text="Mostrar Gráfico", command=mostrar_grafico, font=("Arial", 12, "bold"))
boton_mostrar.pack(pady=10)

# Ejecutar la ventana
root.mainloop()
