#Python Coding by Monkey Python Coding Circus of Alan.RG.Systemas
"""
    
    Forex Market Monitor
    (show at one screen the relevantest market's on the World)
    
    #self.versionado=[v.9.8]

"""
import sys, os
import pytz
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QHBoxLayout, QLabel,
    QLineEdit, QGridLayout, QVBoxLayout, QWidget, QSlider,
    QProgressBar, QAction, QDialog, QPushButton
)
from PyQt5.QtCore import QTimer, QTime, Qt, QPoint, QPointF
from PyQt5.QtGui import QFont, QIcon, QPainter, QPen, QPolygon, QPalette, QColor
import math
from math import cos, sin, pi
import json

class MarketHoursDialog(QDialog):
    '''
        Dialogo para configurar los horarios de los mercados
        
    uso:
        MarketHoursDialog(dic horarios del mercado)
    '''
    def __init__(self, market_hours):
        super().__init__()
        self.market_hours = market_hours
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Configurar Horarios")
        # Aplicar un color de fondo negro a la ventana principal
        self.setStyleSheet("background-color: black;")
        self.setFixedSize(300,180)
        
        layout = QVBoxLayout()

        grid_layout = QGridLayout()
        for row, (market, hours) in enumerate(self.market_hours.items()):
            market_label = QLabel(market)
            open_time_edit = QLineEdit(hours[0])
            close_time_edit = QLineEdit(hours[1])
            
            market_label.setFont(QFont('Roboto'))
            market_label.setStyleSheet(f"color: white; background: black; font-weight: bold")
            
            open_time_edit.setFont(QFont('Roboto'))
            open_time_edit.setStyleSheet(f"color: black; background: darkgrey; font-weight: bold")
            open_time_edit.setFixedSize(50,20)
            
            close_time_edit.setFont(QFont('Roboto'))
            close_time_edit.setStyleSheet(f"color: black; background: darkgrey; font-weight: bold")
            close_time_edit.setFixedSize(50,20)

            grid_layout.addWidget(market_label, row, 0)
            grid_layout.addWidget(open_time_edit, row, 1)
            grid_layout.addWidget(close_time_edit, row, 2)

        layout.addLayout(grid_layout)

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_hours)
        save_button.setStyleSheet("background-color: darkgrey; color: black;")
        
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_hours(self):
        for row in range(self.layout().count()):
            layout_item = self.layout().itemAt(row)
            if layout_item is not None:
                if isinstance(layout_item, QGridLayout):
                    for row in range(layout_item.rowCount()):
                        market_name_label = layout_item.itemAtPosition(row, 0).widget()
                        market_name = market_name_label.text()
                        open_time_edit = layout_item.itemAtPosition(row, 1).widget()
                        close_time_edit = layout_item.itemAtPosition(row, 2).widget()
                        if self.validate_time_format(open_time_edit.text()) and self.validate_time_format(close_time_edit.text()):
                            self.market_hours[market_name] = [open_time_edit.text(), close_time_edit.text()]
        #print('horarios actuualizados localmente:', self.market_hours)
        self.accept()
    
    def validate_time_format(self, time_str):
        try:
            hours, minutes = map(int, time_str.split(':'))
            return 0 <= hours <= 23 and 0 <= minutes <= 59
        except ValueError:
            return False

class ConfigManager:
    '''
        Manejo de la configuraicion a archivo
    '''
    def __init__(self, filename="config.json"):
        self.filename = filename
        self.config_data = None
        self.load_config()

    def load_config(self):
        try:
            print("Intentando cargar la configuración...")
            with open(self.filename, "r") as config_file:
                self.config_data = json.load(config_file)
                print("¡Archivo de configuración cargado correctamente!")
                QMessageBox.information(QMessageBox(),'Carga de Configuración Completa', 'Configuración Cargada Exitosamente!')
        except FileNotFoundError:
            # Configuración por defecto si el archivo no existe
            print("Archivo de configuración no encontrado. Se carga la configuración por defecto...")
            QMessageBox.information(QMessageBox(),'Archivo de Configuración no Existe', 'Archivo de configuración no encontrado, Se carga la configuración por defecto...')
            self.config_data = {
                "market_hours": {
                    # Definir los horarios de los mercados por defecto aquí, eliminar el archivo de configuración antes de correr el programa
                    "NewYork.UTC-4": ["09:30", "16:00"], #apertura Y cierre confirmados
                    "Argentina.UTC-3": ["11:00", "17:00"], #apertura y cierre confirmados
                    "London.UTC": ["08:00", "17:00"], 
                    "Tokyo.UTC+9": ["08:00", "17:00"],
                    "Sydney.UTC+11": ["08:00", "17:00"] #apertura ok
                },
                "colores_app": {
                    # Definir más colores por defecto aquí, eliminar el archivo de configuración antes de correr el programa
                    "color_barra_open": "green",
                    "color_barra_close": "red",
                    "color_fondo_barra_open": "darkred",
                    "color_fondo_barra_close": "darkgreen",
                    "color_fondo_barra_close_findeoferiado": "darkred",
                    "color_texto_barra": "white",
                    "color_cuadrante_reloj": "black",
                    "color_indicador_open_reloj": "green",
                    "color_indicador_close_reloj": "darkred",
                    "color_ahuja_hora_reloj": "blue",
                    "color_ahuja_minuto_reloj": "yellow",
                    "color_ahuja_segundo_reloj": "white",
                    "color_texto_horarios_del_mercado_open": "#00FF00",
                    "color_texto_horarios_del_mercado_close": "red",
                    "color_texto_hora_open": "#00FF00",
                    "color_texto_hora_close": "red",
                    "color_texto_mercado_open": "#00FF00",
                    "color_texto_mercado_close": "red",
                    "color_texto_fecha_open": "#00FF00",
                    "color_texto_fecha_close": "red",
                    "color_texto_diasemana_open": "#00FF00",
                    "color_texto_diasemana_close": "red",
                    "color_fondo_textos": "black"
                }
            }
            self.save_config()

    def save_config(self):
        with open(self.filename, "w") as config_file:
            json.dump(self.config_data, config_file, indent=4)
            print("¡Configuración guardada!")
            QMessageBox.information(QMessageBox(), 'Configuración Guardada', 'Configuración Guardada Exitosamente!')

    def get_color(self):
        return self.config_data["colores_app"]

    def set_color(self, key, color_name):
        #corregir
        self.config_data["colors"][key] = color_name

    def get_market_hours(self):
        return self.config_data["market_hours"]
    
    def set_market_hours(self, markets_hours):
        self.config_data["market_hours"] = markets_hours

class AnalogClockWidget(QWidget):
    def __init__(self, timezone, market_hour_ini, market_hour_end, colores_app):
        super().__init__()
        self.timezone = timezone
        self.market_hour_ini = market_hour_ini
        self.market_hour_end = market_hour_end
        self.colores_app = colores_app

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # Actualiza cada 1000 ms (1 segundo)

        # Establecer un color de fondo negro
        self.setStyleSheet("background-color: black;")

    def paintEvent(self, event):
        timenow = datetime.now(pytz.timezone(self.timezone))
        hora_minuto = timenow.strftime("%H:%M")
        dia_semana = timenow.strftime("%A")
        hora = timenow.strftime("%H")
        minuto = timenow.strftime("%M")
        segundo = timenow.strftime("%S")
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Centro del reloj
        rect = event.rect()
        # Coordenadas del centro del círculo del reloj
        center = self.rect().center()

        # Ancho y altura del rectángulo
        rect_width = self.rect().width()
        rect_height = self.rect().height()

        # Coordenadas de los vértices del triángulo
        top_vertex = QPointF(center)
        left_vertex = QPointF(0 , rect_height)
        right_vertex = QPointF(rect_width, rect_height)

        # Dibujar el triángulo
        painter.setPen(Qt.darkGray)
        painter.setBrush(Qt.black)
        polygon = QPolygon([top_vertex.toPoint(), left_vertex.toPoint(), right_vertex.toPoint()])
        painter.drawPolygon(polygon)

        # Configuración del fondo del reloj
        painter.setPen(QPen(Qt.darkGray, 1))
        painter.setBrush(QColor(self.colores_app["color_cuadrante_reloj"]))
        painter.drawEllipse(center, 87, 87)
        
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse (center, 87, 87)

        painter.setPen(Qt.NoPen)
        if self.market_hour_ini <= hora_minuto < self.market_hour_end and dia_semana != "domingo" and dia_semana != "sábado":
            painter.setBrush(QColor(self.colores_app["color_indicador_open_reloj"]))
            painter.drawEllipse(center, 55, 55)
        else:
            painter.setBrush(QColor(self.colores_app["color_indicador_close_reloj"]))
            painter.drawEllipse(center, 55, 55)

        # Configuración de la brocha para las manecillas
        painter.setBrush(Qt.black)

        # Dibujar manecilla del minuto
        minute_angle = (90 - int(minuto) * 6) % 360
        minute_point = center + QPointF(70 * cos(minute_angle * pi / 180), -70 * sin(minute_angle * pi / 180))
        #painter.setPen(QPen(Qt.yellow, 4))
        painter.setPen(QPen(QColor(self.colores_app["color_ahuja_minuto_reloj"]), 4))
        painter.drawLine(center, minute_point)

        # Dibujar manecilla del segundo
        second_angle = (90 - int(segundo) * 6) % 360
        second_point = center + QPointF(70 * cos(second_angle * pi / 180), -70 * sin(second_angle * pi / 180))
        painter.setPen(QPen(QColor(self.colores_app["color_ahuja_segundo_reloj"]), 1))
        painter.drawLine(center, second_point)

        # Dibujar los círculos para las horas
        painter.setPen(QPen(Qt.white, 2))
        for hour in range(12):
            hour_angle = (90 - hour * 30) % 360
            hour_point = center + QPointF(80 * cos(hour_angle * pi / 180), -80 * sin(hour_angle * pi / 180))
            painter.drawEllipse(hour_point, 2, 2)

        # Dibujar las líneas para los minutos
        painter.setPen(QPen(Qt.white, 1))
        for minute in range(0, 60):
            minute_angle = (90 - minute * 6) % 360
            start_point = center + QPointF(75 * cos(minute_angle * pi / 180), -75 * sin(minute_angle * pi / 180))
            end_point = center + QPointF(85 * cos(minute_angle * pi / 180), -85 * sin(minute_angle * pi / 180))
            painter.drawLine(start_point, end_point)

        # Dibujar manecilla de la hora
        hour_angle = (90 - int(hora) * 30) % 360
        hour_point = center + QPointF(55 * cos(hour_angle * pi / 180), -55 * sin(hour_angle * pi / 180))
        painter.setPen(QPen(QColor(self.colores_app["color_ahuja_hora_reloj"]), 12))
        painter.drawLine(center, hour_point)
        painter.setPen(QPen(QColor(self.colores_app["color_ahuja_hora_reloj"]), 14))
        painter.drawEllipse(center, 7, 7)

class ForexMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Python Coding by Monkey Python Coding Circus of Alan.RG.Systemas")
        self.setWindowTitle("Forex Monitor v.9.8")
        #self.setGeometry(0, 0, 1280, 360)
        self.setFixedSize(1280, 380)

        self.config_manager = ConfigManager()
        self.market_hours = self.config_manager.get_market_hours() # carga de horarios de mercado por defecto o de archivo de configuracion
        self.colores_app = self.config_manager.get_color() # carga de colores por defecto o de archivo de configuracion
        #print(self.colores_app)

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        # Establecer un icono de aplicacion
        self.IconPath = os.path.join(scriptDir, 'icons')   
        self.setWindowIcon(QIcon(self.IconPath + os.path.sep + 'fc.png'))
        # Establecer una imagen de fondo
        self.ImagePath = os.path.join(scriptDir, 'images')   
        self.setStyleSheet("background-image: url('" + self.ImagePath + os.path.sep + "fondo_1280x720.png');")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        market_dates_layout = QHBoxLayout()
        market_dia_semana_layout = QHBoxLayout()
        market_times_layout = QHBoxLayout()
        market_analogclock_layout = QHBoxLayout()
        market_names_layout = QHBoxLayout()
        market_progress_layout = QHBoxLayout()
        market_progress_label_layout = QHBoxLayout()
        market_active_time_layout = QHBoxLayout()
        menubar_layout =  QHBoxLayout()
        
        #self.main_layout.addLayout(market_active_time_layout)        
        self.main_layout.addLayout(market_progress_layout)
        self.main_layout.addLayout(market_progress_label_layout)
        self.main_layout.addLayout(market_analogclock_layout)
        self.main_layout.addLayout(market_times_layout)
        self.main_layout.addLayout(market_names_layout)
        self.main_layout.addLayout(market_dates_layout)
        self.main_layout.addLayout(market_dia_semana_layout)
        self.main_layout.addLayout(menubar_layout)

        # Aplicar un color de fondo negro a la ventana principal
        #self.setStyleSheet("background-color: black;")

        self.timezone_mapping = {
            "NewYork.UTC-4": "America/New_York",
            "Argentina.UTC-3": "America/Argentina/Buenos_Aires",
            "London.UTC": "Europe/London",
            "Tokyo.UTC+9": "Asia/Tokyo",
            "Sydney.UTC+11": "Australia/Sydney"
        }

        '''
        #agregar funcion para configurar hora de apertura y cierre de cada mercado desde la app
        self.market_hours = {
            "NewYork.UTC-4": ["09:30", "16:00"], #apertura Y cierre confirmados
            "Argentina.UTC-3": ["11:00", "17:00"], #apertura y cierre confirmados
            "London.UTC": ["08:00", "17:00"], 
            "Tokyo.UTC+9": ["08:00", "17:00"],
            "Sydney.UTC+11": ["08:00", "17:00"] #apertura ok
        }
        '''

        #Diccionarios y Campos de datos en formato Qlabel // DISEÑO UI
        self.market_names = {}
        self.market_date = {}
        self.market_dia_semana = {}
        self.market_clock = {}
        self.clock_analog_widget = {}
        self.progress_bar_widget = {}
        self.label_progress_bar = {}
        self.market_open_time = {}
        self.market_close_time = {}
        
        for market in self.timezone_mapping:
            #open an close hours of market
            self.market_open_time[market] = QLabel("open_time",self)
            self.market_close_time[market] = QLabel("close_time",self)
            self.market_open_time[market].setFixedSize(40,15)
            self.market_close_time[market].setFixedSize(40,15)
            self.market_close_time[market].setAlignment(Qt.AlignCenter)
            self.market_open_time[market].setFont(QFont('Roboto',10, QFont.Bold))
            self.market_close_time[market].setFont(QFont('Roboto',10, QFont.Bold))
            market_active_time_layout.addWidget(self.market_open_time[market])
            market_active_time_layout.addWidget(self.market_close_time[market])

            self.progress_bar_widget[market] = QProgressBar(self)
            self.progress_bar_widget[market].setFont(QFont('Roboto', 10, QFont.Bold))
            self.progress_bar_widget[market].setRange(0, 100)  # Definimos un rango inicial para el slider
            self.progress_bar_widget[market].setFixedSize(200, 12) 
            market_progress_layout.addWidget(self.progress_bar_widget[market])
            
            self.label_progress_bar[market] = QLabel(self)
            self.label_progress_bar[market].setFont(QFont('Roboto'))
            self.label_progress_bar[market].setFixedSize(200, 10)
            self.label_progress_bar[market].setAlignment(Qt.AlignCenter)
            market_progress_label_layout.addWidget(self.label_progress_bar[market])

            self.clock_analog_widget[market] = AnalogClockWidget(self.timezone_mapping[market],self.market_hours[market][0],self.market_hours[market][1], self.colores_app)
            self.clock_analog_widget[market].setFixedSize(200, 200)  # Ajustamos el tamaño del reloj
            market_analogclock_layout.addWidget(self.clock_analog_widget[market])

            self.market_date[market] = QLabel("Fecha", self)
            self.market_date[market].setFont(QFont('Lora', 18, QFont.Bold))
            self.market_date[market].setFixedSize(180,18)
            self.market_date[market].setAlignment(Qt.AlignCenter)
            market_dates_layout.addWidget(self.market_date[market])

            self.market_dia_semana[market] = QLabel("Dia Semana", self)
            self.market_dia_semana[market].setFont(QFont('Lora', 12, QFont.Bold))
            self.market_dia_semana[market].setFixedSize(180,20)
            self.market_dia_semana[market].setAlignment(Qt.AlignCenter)
            market_dia_semana_layout.addWidget(self.market_dia_semana[market])
            
            self.market_clock[market] = QLabel("Hora", self)
            self.market_clock[market].setFont(QFont('Lora', 28, QFont.Bold))
            self.market_clock[market].setFixedSize(180,28)
            self.market_clock[market].setAlignment(Qt.AlignCenter)
            market_times_layout.addWidget(self.market_clock[market])
            
            self.market_names[market] = QLabel(f"Mercado", self)
            self.market_names[market].setFont(QFont('Roboto', 14, QFont.Bold))
            self.market_names[market].setFixedSize(180,20)
            self.market_names[market].setAlignment(Qt.AlignCenter)
            market_names_layout.addWidget(self.market_names[market])

        # Barra de menú
        self.menuBar = self.menuBar()
        # Establecer estilo para la barra de menú
        self.menuBar.setStyleSheet("background-color: black; color: white;") # Ajusta el color de fondo y el color del texto de la barra de menú
        # Menú Forex Monitor
        self.fmonitor = self.menuBar.addMenu('Forex Monitor')
        self.opciondonar = QAction('Donar', self)
        self.fmonitor.addAction(self.opciondonar)
        self.opcionsalir = QAction('Salir', self)
        self.fmonitor.addAction(self.opcionsalir)
        # Menú Configuración
        self.menuConfiguracion = self.menuBar.addMenu('Configuración')
            # Opción para configurar las horas de apertura y cierre de cada mercado
        self.opcionHorarios = QAction('Configurar Horarios de los Mercados', self)
        self.opcionHorarios.triggered.connect(self.configurar_horarios)
        self.menuConfiguracion.addAction(self.opcionHorarios)
            # Opción para configurar los colores de los elementos de la aplicación
        self.opcionColores = QAction('Configurar Colores de la Aplicación', self)
        self.opcionColores.triggered.connect(self.configurar_colores)
        self.menuConfiguracion.addAction(self.opcionColores)
        # Agregamos la barra al layout inferior
        menubar_layout.addWidget(self.menuBar)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_markets)
        self.timer.start(1000)  # Actualiza cada 1000 ms (1 segundo)
        self.update_markets()  # Actualiza los mercados al iniciar

    def configurar_horarios(self):
        # Implementar la lógica para configurar las horas de apertura y cierre de cada mercado
        #QMessageBox.information(QMessageBox(),'Configurar Horarios de Mercado', '¡Implementando Metodos y Clases!')
        #print("Para Configurar Horarios de Mercado... Implementar configurar_horarios")
        dialog = MarketHoursDialog(self.market_hours)
        if dialog.exec_() == QDialog.Accepted:
            self.market_hours = dialog.market_hours
            self.config_manager.config_data["market_hours"]= dialog.market_hours
            self.config_manager.save_config()
            #self.update_interface()   #la app lo hace automaticante cada segundo con update_markets

    def configurar_colores(self):
        # Implementar la lógica para configurar los colores de los elementos de pantalla
        QMessageBox.information(QMessageBox(),'Configurar Colores', '¡Implementando Metodos y Clases!')
        print("Para Configurar Colores... Implementar configurar_colores")
        '''
        color = QColorDialog.getColor()
        if color.isValid():
            color_name = color.name()
            print("¡Color:", color_name, "Seteado como Color de Fondo!")
            self.config_manager.set_color("widget_fondo", color_name)
            self.update_interface()
            self.config_manager.save_config()
        '''

    def update_interface(self):
        # Actualizar la interfaz gráfica con la nueva configuración, ver update_markets
        QMessageBox.information(QMessageBox(),'Interfaz Actualizada', '¡Implementando Metodos y Clases!')
        print("Para Actualizar Interface... Implementar configurar_colores")
        '''
        for market, hours in self.market_hours.items():
            self.label[market].setText(f"{market}: {hours[0]} - {hours[1]}")
        color_widget_fondo = self.config_manager.get_color("widget_fondo")
        self.widget.setStyleSheet(f"background-color: {color_widget_fondo};")
        print("Interfaz actualizada")
        QMessageBox.information(QMessageBox(), 'Interfaz Actualizada', 'Interfaz Actualizada exitosamente!')
        '''

    def mercado_abierto(self, zona_horaria, hora_apertura, hora_cierre, market):
        hora_actual = datetime.now(pytz.timezone(zona_horaria))
        dia_semana = hora_actual.strftime("%A")
        hora_apertura = hora_actual.replace(hour=int(hora_apertura.split(":")[0]), minute=int(hora_apertura.split(":")[1]), second=0)
        hora_cierre = hora_actual.replace(hour=int(hora_cierre.split(":")[0]), minute=int(hora_cierre.split(":")[1]), second=0)
        #print(dia_semana)
        #print(dia_semana != "domingo" and dia_semana != "sábado")
        return hora_apertura <= hora_actual <= hora_cierre and dia_semana != "domingo" and dia_semana != "sábado"

    def estado_mercado(self, zona_horaria, apertura, cierre, market):
        if self.mercado_abierto(zona_horaria, apertura, cierre, market):
            #return '#00FF00', "black", "darkred" #colorestado, fondoetiqueta, fondobarra, estadobarra
            return (
                self.colores_app["color_texto_hora_open"],  # colorestado
                self.colores_app["color_fondo_textos"],     # fondoetiqueta
                self.colores_app["color_fondo_barra_open"], # fondobarra
                self.colores_app["color_barra_open"]        # estadobarra
            )
        else:
            #return "red", "black", "darkgreen" #'#333333' <--- gris oscuro;  '#00FF00' <--- verde matrix
            return (
                self.colores_app["color_texto_hora_close"],
                self.colores_app["color_fondo_textos"],
                self.colores_app["color_fondo_barra_close"],
                self.colores_app["color_barra_close"]
            )

    def donde_este_el_relojanalogico_pongo_el_horario_del_mercado(self):
        for market in self.market_names:
            # Aquí calculamos la posición relativa a la ventana principal para el reloj analógico
            pos_analogclock = self.clock_analog_widget[market].mapTo(self.central_widget, QPoint(0, 0))
            # Ajustamos la posición de los widgets de apertura y cierre en relación con la posición del reloj analógico
            clock_width = self.clock_analog_widget[market].width()  # Obtener el ancho del reloj analógico
            clock_height = self.clock_analog_widget[market].height()  # Obtener la altura del reloj analógico
            open_time_x = pos_analogclock.x() + clock_width -170# Ajustar la posición x para el widget de apertura
            open_time_y = pos_analogclock.y() + 180 # Mantener la misma posición y que el reloj analógico
            close_time_x = pos_analogclock.x() + clock_width -70 # Ajustar la posición x para el widget de cierre
            close_time_y = pos_analogclock.y() + 180  # Mantener la misma posición y que el reloj analógico
            # Movemos los widgets de apertura y cierre a sus nuevas posiciones
            self.market_open_time[market].move(open_time_x, open_time_y)
            self.market_close_time[market].move(close_time_x, close_time_y)
        
    def update_markets(self):
        for market, timezone in self.timezone_mapping.items():
            self.market_open_time[market].setText(self.market_hours[market][0])
            self.market_close_time[market].setText(self.market_hours[market][1])
            current_datetime = datetime.now(pytz.timezone(timezone))
            hora = int(current_datetime.strftime("%H"))
            minuto = int(current_datetime.strftime("%M"))
            dia_semana = current_datetime.strftime("%A")
            local_time = current_datetime.strftime("%H:%M:%S")# (%Z)")
            local_date = current_datetime.strftime('%d/%m/%Y')
            self.market_names[market].setText(f"  {market}  ")
            self.market_date[market].setText(f"  {local_date}  ")
            self.market_dia_semana[market].setText(f"  {dia_semana}  ")
            self.market_clock[market].setText(f"  {local_time}  ")
            # eb este punto se llama a estado_mercado ver
            colorestado, fondoetiqueta, fondobarra, estadobarra = self.estado_mercado(timezone, self.market_hours[market][0], self.market_hours[market][1], market)
            self.market_open_time[market].setStyleSheet(f"color: {colorestado}; background: {fondoetiqueta}; font-weight: bold")
            self.market_close_time[market].setStyleSheet(f"color: {colorestado}; background: {fondoetiqueta}; font-weight: bold")
            self.market_names[market].setStyleSheet(f"color: {colorestado}; background: {fondoetiqueta}; font-weight: bold")
            self.market_date[market].setStyleSheet(f"color: {colorestado}; background: {fondoetiqueta}; font-weight: bold")
            self.market_dia_semana[market].setStyleSheet(f"color: {colorestado}; background: {fondoetiqueta}; font-weight: bold")
            self.market_clock[market].setStyleSheet(f"color: {colorestado}; background: {fondoetiqueta}; font-weight: bold")
            self.progress_bar_widget[market].setStyleSheet(f"""
                QProgressBar {{
                    background-color: {fondobarra}; /* Color de fondo de la barra de progreso*/
                    text-align: center; /* Alineación del texto al centro */
                    font-family: "Roboto", sans-serif; /* Fuente Roboto */
                    color: lightgray; /* Color del texto */
                    font-weight: bold; /* Texto en negrita */
                }}
                QProgressBar::chunk {{
                    background-color: {estadobarra}; /* Color de la barra de progreso */
                }}
            """)
            self.label_progress_bar[market].setStyleSheet(f"color: {colorestado}; background: {fondoetiqueta}; font-weight: bold")
            self.update_progress_bars(market, timezone, hora, minuto, dia_semana)
            self.donde_este_el_relojanalogico_pongo_el_horario_del_mercado() #busca la hubicacion de los relojes
            
    def moveEvent(self, event):
        super().moveEvent(event)
        self.donde_este_el_relojanalogico_pongo_el_horario_del_mercado()
        #self.update_markets()

    def horas_a_minutos(self, lista_horas):
        lista_minutos = []
        for hora_str in lista_horas:
            hora_obj = datetime.strptime(hora_str, "%H:%M")
            minutos = hora_obj.hour * 60 + hora_obj.minute
            lista_minutos.append(int(minutos))
        return lista_minutos

    def update_progress_bars(self, market, timezone, current_hour, current_minute,dia_semana):
        #VER SI ESTA ES UNA MEJOR EVALUACION DEL ESTADO DEL MERCADO (ABIERTO O CERRADO)
        list_market_in_minutes = self.horas_a_minutos(self.market_hours[market])
        #print(market, ":", list_market_in_minutes)
        open_market_in_minutes = list_market_in_minutes[0]
        close_market_in_minutes = list_market_in_minutes[1]
        total_market_minutes = close_market_in_minutes - open_market_in_minutes
        total_out_market_minutes = 24 * 60 - total_market_minutes
        current_time_in_minutes = current_hour * 60 + current_minute 
        #si la hora actual se encuentra en el rango horario de mercado abierto
        if open_market_in_minutes <= current_time_in_minutes < close_market_in_minutes: 
            elapsed_minutes = current_time_in_minutes - open_market_in_minutes
            fraction = elapsed_minutes / total_market_minutes
            porcent = int(100 * (1 - fraction))
            self.progress_bar_widget[market].setValue(porcent)
            remain_open_minutes = close_market_in_minutes - current_time_in_minutes
            self.label_progress_bar[market].setText(f'Abierto! Quedan: {remain_open_minutes} minutos')
        #si la hora actual esta fuera del rango horario de mercado abierto 
        else:
            #si la hora actual es menor a la hora de apertura del mercado
            if current_time_in_minutes < open_market_in_minutes:
                # Tiempo restante hasta la próxima apertura
                remain_close_minutes = open_market_in_minutes - current_time_in_minutes
            #si no
            else: 
                # Tiempo restante hasta la próxima apertura del día siguiente
                remain_close_minutes = total_out_market_minutes - (current_time_in_minutes - close_market_in_minutes)
            fraction = remain_close_minutes / total_out_market_minutes
            porcent = int(100 * (1 - fraction))
            self.progress_bar_widget[market].setValue(100 - porcent)
            self.label_progress_bar[market].setText('Cerrado! {} minutos para abrir'.format(remain_close_minutes))
        #print(market,dia_semana)
        if dia_semana == "viernes" and current_time_in_minutes > close_market_in_minutes:
            self.label_progress_bar[market].setText('Cerrado! mañana es sabado')
            self.barra_fuera_de_mercado(market)
            porcent = int(100 * (1 - 0))
            self.progress_bar_widget[market].setValue(100 - porcent)

        if dia_semana == "sábado" or (dia_semana == "domingo" and current_time_in_minutes < close_market_in_minutes):
            self.label_progress_bar[market].setText('Cerrado! es {}!'.format(dia_semana))
            self.barra_fuera_de_mercado(market)
            porcent = int(100 * (1 - 0))
            self.progress_bar_widget[market].setValue(100 - porcent)
        #print(market, remain_minutes, "/", total_out_market_minutes)
            
    def barra_fuera_de_mercado(self, market):
        self.progress_bar_widget[market].setStyleSheet(f"""
                QProgressBar {{
                    background-color: darkred; /* Color de fondo de la barra de progreso*/
                    text-align: center; /* Alineación del texto al centro */
                    font-family: "Roboto", sans-serif; /* Fuente Roboto */
                    color: lightgray; /* Color del texto */
                    font-weight: bold; /* Texto en negrita */
                }}
                QProgressBar::chunk {{
                    background-color: gray; /* Color de la barra de progreso */
                }}
            """)
        self.label_progress_bar[market].setStyleSheet(f"color: red; background: black; font-weight: bold")

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fc8 = ForexMonitor()
    fc8.show()
    sys.exit(app.exec_())
