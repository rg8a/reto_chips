import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib
import random
import math
import csv
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')

nombre_archivo = 'comportamiento_tractor.csv'

if not os.path.exists(nombre_archivo):
    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(['VelocidadAngular (rad/s)', 'RadioRueda (m)', 'RelacionTransmision', 'RPM'])

# Inicializar listas de datos
velocidades, radios, relaciones, rpms = [], [], [], []

def generar_dato():
    velocidad_angular = round(random.uniform(5, 20), 2)
    radio_rueda = round(random.uniform(0.3, 1.2), 2)
    relacion_transmision = random.randint(5, 15)
    rpm = round((velocidad_angular * 60) / (2 * math.pi * radio_rueda * relacion_transmision), 2)

    with open(nombre_archivo, mode='a', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow([velocidad_angular, radio_rueda, relacion_transmision, rpm])

    # Agregar a listas
    velocidades.append(velocidad_angular)
    radios.append(radio_rueda)
    relaciones.append(relacion_transmision)
    rpms.append(rpm)

def crear_figura(tipo):
    fig, ax = plt.subplots(figsize=(6, 4))
    if tipo == 0:
        ax.scatter(velocidades, rpms, color='blue')
        ax.set_title("RPM vs Velocidad Angular")
        ax.set_xlabel("Velocidad Angular (rad/s)")
        ax.set_ylabel("RPM")
    elif tipo == 1:
        ax.scatter(radios, rpms, color='green')
        ax.set_title("RPM vs Radio de Rueda")
        ax.set_xlabel("Radio de Rueda (m)")
        ax.set_ylabel("RPM")
    elif tipo == 2:
        ax.scatter(relaciones, rpms, color='red')
        ax.set_title("RPM vs Relación de Transmisión")
        ax.set_xlabel("Relación de Transmisión")
        ax.set_ylabel("RPM")
    ax.grid(True)
    return fig

def draw_figure(canvas_elem, figure):
    canvas = FigureCanvasTkAgg(figure, canvas_elem.TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return canvas

# Layout de PySimpleGUI
layout = [
    [sg.Text('Simulación del comportamiento del tractor')],
    [sg.Button('Iniciar Simulación'), sg.Button('Cambiar Gráfica'), sg.Button('Salir')],
    [sg.Canvas(key='-CANVAS-')],
]

window = sg.Window("Visualización en Tiempo Real", layout, finalize=True)

canvas_elem = window['-CANVAS-']
grafica_actual = 0
fig = crear_figura(grafica_actual)
canvas = draw_figure(canvas_elem, fig)

simulacion_activa = False

while True:
    event, values = window.read(timeout=1000)

    if event in (sg.WIN_CLOSED, 'Salir'):
        break

    if event == 'Iniciar Simulación':
        simulacion_activa = True

    if event == 'Cambiar Gráfica':
        grafica_actual = (grafica_actual + 1) % 3
        fig.clf()
        fig = crear_figura(grafica_actual)
        canvas.get_tk_widget().destroy()
        canvas = draw_figure(canvas_elem, fig)

    if simulacion_activa and event == '__TIMEOUT__':
        generar_dato()
        fig.clf()
        fig = crear_figura(grafica_actual)
        canvas.get_tk_widget().destroy()
        canvas = draw_figure(canvas_elem, fig)

window.close()
