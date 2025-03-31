import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib
import random
import math
import csv
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración de matplotlib
matplotlib.use('TkAgg')

# Nombre del archivo CSV
nombre_archivo = 'comportamiento_tractor.csv'

# Inicializa CSV con encabezados si no existe
if not os.path.exists(nombre_archivo):
    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(['VelocidadAngular (rad/s)', 'RadioRueda (m)', 'RelacionTransmision', 'RPM'])

# Función para generar un nuevo dato
def generar_dato():
    velocidad_angular = round(random.uniform(5, 20), 2)
    radio_rueda = round(random.uniform(0.3, 1.2), 2)
    relacion_transmision = random.randint(5, 15)
    rpm = round((velocidad_angular * 60) / (2 * math.pi * radio_rueda * relacion_transmision), 2)
    
    with open(nombre_archivo, mode='a', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow([velocidad_angular, radio_rueda, relacion_transmision, rpm])

    return velocidad_angular, rpm

# Función para crear una figura de matplotlib
def crear_figura(xs, ys):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(xs, ys, color='blue')
    ax.set_title("RPM vs Velocidad Angular")
    ax.set_xlabel("Velocidad Angular (rad/s)")
    ax.set_ylabel("RPM")
    ax.grid(True)
    return fig

# Función para dibujar la figura dentro de PySimpleGUI
def draw_figure(canvas_elem, figure):
    canvas = FigureCanvasTkAgg(figure, canvas_elem.TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return canvas

# Elementos del layout de la ventana
layout = [
    [sg.Text('Simulación del comportamiento del tractor')],
    [sg.Button('Iniciar Simulación'), sg.Button('Salir')],
    [sg.Canvas(key='-CANVAS-')],
]

# Crear la ventana
window = sg.Window("Visualización en Tiempo Real", layout, finalize=True)

# Inicializar datos
xs, ys = [], []
canvas_elem = window['-CANVAS-']
fig = crear_figura(xs, ys)
canvas = draw_figure(canvas_elem, fig)

# Loop de eventos
while True:
    event, values = window.read(timeout=1000)  # Cada 1 segundo

    if event == sg.WIN_CLOSED or event == 'Salir':
        break

    if event == 'Iniciar Simulación':
        xs.clear()
        ys.clear()
        fig.clf()
        canvas.get_tk_widget().destroy()
        canvas = draw_figure(canvas_elem, crear_figura(xs, ys))

    if event is None or event == '__TIMEOUT__':
        # Generar un nuevo punto y actualizar gráfica
        velocidad_angular, rpm = generar_dato()
        xs.append(velocidad_angular)
        ys.append(rpm)

        fig.clf()
        fig = crear_figura(xs, ys)
        canvas.get_tk_widget().destroy()
        canvas = draw_figure(canvas_elem, fig)

window.close()
