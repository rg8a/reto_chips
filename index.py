# -----------------------------
# Importación de bibliotecas
# -----------------------------
import PySimpleGUI as sg                     # Librería para crear interfaces gráficas simples
import matplotlib.pyplot as plt              # Para graficar
import matplotlib                            # Backend de Matplotlib
import random                                # Para generar datos aleatorios
import math                                  # Para operaciones matemáticas
import csv                                   # Para leer/escribir archivos CSV
import os                                    # Para operaciones con archivos y directorios
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Integración de Matplotlib con Tkinter/PySimpleGUI

# -----------------------------
# Configuración de Matplotlib
# -----------------------------
matplotlib.use('TkAgg')  # Usar el backend TkAgg (compatible con PySimpleGUI)

# -----------------------------
# Archivo donde se guardan los datos
# -----------------------------
nombre_archivo = 'comportamiento_tractor.csv'

# Crear el archivo CSV si no existe, con encabezados
if not os.path.exists(nombre_archivo):
    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(['VelocidadAngular (rad/s)', 'RadioRueda (m)', 'RelacionTransmision', 'RPM'])

# -----------------------------
# Inicializar listas para almacenar los datos simulados
# -----------------------------
velocidades, radios, relaciones, rpms = [], [], [], []

# -----------------------------
# Función para generar un nuevo punto de datos aleatorios
# -----------------------------
def generar_dato():
    # Se generan valores aleatorios simulando sensores de un tractor
    velocidad_angular = round(random.uniform(5, 20), 2)         # radianes por segundo
    radio_rueda = round(random.uniform(0.3, 1.2), 2)            # metros
    relacion_transmision = random.randint(5, 15)                # relación de transmisión
    rpm = round((velocidad_angular * 60) / (2 * math.pi * radio_rueda * relacion_transmision), 2)  # cálculo de RPM

    # Se guarda el nuevo dato en el archivo CSV
    with open(nombre_archivo, mode='a', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow([velocidad_angular, radio_rueda, relacion_transmision, rpm])

    # Se agrega el dato a las listas para graficar en tiempo real
    velocidades.append(velocidad_angular)
    radios.append(radio_rueda)
    relaciones.append(relacion_transmision)
    rpms.append(rpm)

# -----------------------------
# Función que crea la figura de la gráfica según el tipo seleccionado
# tipo = 0 → Velocidad Angular
# tipo = 1 → Radio de Rueda
# tipo = 2 → Relación de Transmisión
# -----------------------------
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

    ax.grid(True)  # Mostrar cuadrícula
    return fig

# -----------------------------
# Función que dibuja una figura de Matplotlib dentro de un Canvas de PySimpleGUI
# -----------------------------
def draw_figure(canvas_elem, figure):
    canvas = FigureCanvasTkAgg(figure, canvas_elem.TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    return canvas

def contar_registros():
    if not os.path.exists(nombre_archivo):
        return 0
    with open(nombre_archivo, mode='r') as archivo_csv:
        return max(0, sum(1 for _ in archivo_csv) - 1)  # Evitar negativos


def reiniciar_datos():
    global velocidades, radios, relaciones, rpms
    velocidades, radios, relaciones, rpms = [], [], [], []

    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(['VelocidadAngular (rad/s)', 'RadioRueda (m)', 'RelacionTransmision', 'RPM'])


# -----------------------------
# Layout de la ventana PySimpleGUI
# -----------------------------
layout = [
    [sg.Text('Simulación del comportamiento del tractor')],
    [sg.Button('Iniciar Simulación'), sg.Button('Cambiar Gráfica'), sg.Button('Salir')],
    [sg.Canvas(key='-CANVAS-')],  # Área donde se mostrará la gráfica
]

# Crear la ventana
window = sg.Window("Visualización en Tiempo Real", layout, finalize=True)

# -----------------------------
# Inicializar la gráfica y su tipo
# -----------------------------
canvas_elem = window['-CANVAS-']
grafica_actual = 0  # Inicia mostrando la primera gráfica (Velocidad Angular)
fig = crear_figura(grafica_actual)  # Crear la figura inicial
canvas = draw_figure(canvas_elem, fig)  # Dibujarla en el canvas

simulacion_activa = False  # Controla si se están generando datos en tiempo real

# -----------------------------
# Bucle principal de eventos
# -----------------------------
while True:
    event, values = window.read(timeout=1000)  # Refrescar cada 1000 ms

    if event in (sg.WIN_CLOSED, 'Salir'):
        break  # Salir del programa

    if event == 'Iniciar Simulación':
        reiniciar_datos()  # Borra CSV y listas
        simulacion_activa = True

    if event == 'Cambiar Gráfica':
        grafica_actual = (grafica_actual + 1) % 3
        fig.clf()
        fig = crear_figura(grafica_actual)
        canvas.get_tk_widget().destroy()
        canvas = draw_figure(canvas_elem, fig)

    if simulacion_activa and event == '__TIMEOUT__':
        if contar_registros() < 100:
            generar_dato()
            fig.clf()
            fig = crear_figura(grafica_actual)
            canvas.get_tk_widget().destroy()
            canvas = draw_figure(canvas_elem, fig)
        else:
            simulacion_activa = False  # Detener la simulación al llegar a 100
            sg.popup("Simulación completada. Se han generado 100 registros.")

# Cerrar la ventana al terminar
window.close()
