import os

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui

from main_interface import Ui_MainWindow
from signals_generator import SignalGenerator
from research_logic import calc_research_bad_alg
from mpl_widget import *
from enums import *
from defaults import *


class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Реализация графического интерфейса основного приложения
    """
    def __init__(self, screen: QtCore.QRect):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)

        # Конфигурация окна приложения
        # Скрытие системных кнопок
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        # Тени
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 92, 157, 550))
        self.centralwidget.setGraphicsEffect(self.shadow)

        # Добавление области масштабирования в правый нижний угол
        QtWidgets.QSizeGrip(self.resize_frame)

        # Перетаскивание окна
        self.header_container.mouseMoveEvent = self.move_window
        self.click_position = None

        # Боковое меню
        self.animation_menu = QtCore.QPropertyAnimation(self.side_menu_container, b"maximumWidth")
        self.animation_geometry = QtCore.QPropertyAnimation(self, b"geometry")

        # Логика
        # Обработчики кнопок
        self.minimized_button.clicked.connect(lambda: self.showMinimized())
        self.close_button.clicked.connect(lambda: self.close())
        self.open_parameters_page_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_page))
        self.open_research_page_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.research_page))
        self.open_function_page_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.function_page))
        self.maximized_button.clicked.connect(self.restore_or_maximized)
        self.side_menu_button.clicked.connect(self.slide_left_menu)
        self.draw_button.clicked.connect(self.draw_main_page_graphics)
        self.start_research_button.clicked.connect(self.start_research_logic)

        # Инициализация значений по умолчанию
        self.full_screen_geometry = screen
        self.last_geometry = None
        self.sampling_rate_edit.setText(DEFAULT_SAMPLING_RATE)
        self.snr_edit.setText(DEFAULT_SNR)
        self.bits_count_edit.setText(DEFAULT_BITS_COUNT)
        self.bits_per_second_edit.setText(DEFAULT_BITS_PER_SECOND)
        self.signal_freq_edit.setText(DEFAULT_SIGNAL_FREQ)
        self.time_delay_edit.setText(DEFAULT_TIME_DELAY)
        self.average_count_edit.setText(DEFAULT_AVERAGE_COUNT)
        self.doppler_edit.setText(DEFAULT_DOPPLER)
        self.signal_generator = SignalGenerator()

        # Обработка событий редактирования параметров
        self.sampling_rate_edit.textChanged.connect(self.sr_change_logic)
        self.bits_count_edit.textChanged.connect(self.bits_count_change_logic)
        self.bits_per_second_edit.textChanged.connect(self.bits_per_second_change_logic)
        self.signal_freq_edit.textChanged.connect(self.signal_freq_change_logic)
        self.time_delay_edit.textChanged.connect(self.time_delay_change_logic)
        self.snr_edit.textChanged.connect(self.snr_change_logic)
        self.doppler_edit.textChanged.connect(self.doppler_change_logic)

        # Инициализация основных графиков
        self.graphics = MplGraphicsModulated()
        self.toolbar = NavigationToolbar(self.graphics, self.graphics, coordinates=True)
        self.verticalLayout_16.addWidget(self.toolbar)
        self.verticalLayout_16.addWidget(self.graphics)

        # Инициализация графика исследования
        self.research_graphics = MplGraphicsResearch()
        self.research_toolbar = NavigationToolbar(self.research_graphics, self.research_graphics, coordinates=True)
        self.verticalLayout_10.addWidget(self.research_toolbar)
        self.verticalLayout_10.addWidget(self.research_graphics)

        # Инициализация графиков функции неопределенности
        self.function_graphics_3d = MplGraphics3dFunction()
        self.function_toolbar_3d = NavigationToolbar(self.function_graphics_3d, self.function_graphics_3d, coordinates=True)
        self.verticalLayout_8.addWidget(self.function_toolbar_3d)
        self.verticalLayout_8.addWidget(self.function_graphics_3d)
        self.function_graphics_2d = MplGraphics2dFunction()
        self.function_toolbar_2d = NavigationToolbar(self.function_graphics_2d, self.function_graphics_2d, coordinates=True)
        self.verticalLayout_12.addWidget(self.function_toolbar_2d)
        self.verticalLayout_12.addWidget(self.function_graphics_2d)

    def draw(self, graph_type: GraphType, x: list, y: list):
        """
        Нарисовать график.
        """
        if graph_type == GraphType.REFERENCE:
            self.graphics.clear_plot_ax1()
            self.graphics.plot_graph_ax1(x, y)
            self.graphics.clear_plot_ax2()
            self.graphics.plot_graph_ax2(x, y)
        elif graph_type == GraphType.RESEARCH:
            self.graphics.clear_plot_ax3()
            self.graphics.plot_graph_ax3(x, y)
            self.graphics.clear_plot_ax4()
            self.graphics.plot_graph_ax4(x, y)
        elif graph_type == GraphType.CORRELATION:
            self.graphics.clear_plot_ax5()
            self.graphics.plot_graph_ax5(x, y)

        self.graphics.draw()
        self.graphics.flush_events()

    def draw_function_3d(self, x: list, y: list, z: list):
        """
        Отобразить взаимную функцию неопределенности.
        """
        self.function_graphics_3d.clear_plot()
        self.function_graphics_3d.plot_graph(x, y, z)
        self.function_graphics_3d.draw()
        self.function_graphics_3d.flush_events()

    def draw_function_2d(self, graph_type: GraphType, x: list, y: list):
        """
        Отобразить двумерные графики взаимной функции неопределенности.
        """
        if graph_type == GraphType.FUNCTION_TAO:
            self.function_graphics_2d.clear_plot_ax1()
            self.function_graphics_2d.plot_graph_ax1(x, y)
        elif graph_type == GraphType.FUNCTION_DOPPLER:
            self.function_graphics_2d.clear_plot_ax2()
            self.function_graphics_2d.plot_graph_ax2(x, y)

        self.function_graphics_2d.draw()
        self.function_graphics_2d.flush_events()

    def draw_criterion_research(self, x: list, y: list):
        """
        Отобразить график исследования.
        """
        self.research_graphics.clear_plot()
        self.research_graphics.plot_graph(x, y)
        self.research_graphics.draw()
        self.research_graphics.flush_events()

    def draw_main_page_graphics(self):
        """
        Отрисовка графиков на главной странице.
        """
        # Расчёт функций
        self.signal_generator.calculate()

        # Отображение эталонного сигнала
        self.draw(GraphType.REFERENCE,
                  self.signal_generator.reference_mod[0],
                  self.signal_generator.reference_mod[1])

        # Отображение исследуемого сигнала
        self.draw(GraphType.RESEARCH,
                  self.signal_generator.research_mod[0],
                  self.signal_generator.research_mod[1])

        # Отображение корреляционной функции
        self.draw(GraphType.CORRELATION,
                  self.signal_generator.correlation[0],
                  self.signal_generator.correlation[1])

        # Вывод найденной оценки времени
        self.time_delay_assessment_edit.setText(str(self.signal_generator.found_time_delay))
        # Отображение взаимной функции неопределенности
        self.draw_function_3d(self.signal_generator.fn3d[0],
                              self.signal_generator.fn3d[1],
                              self.signal_generator.fn3d[2])
        self.draw_function_2d(GraphType.FUNCTION_TAO,
                              self.signal_generator.fn2d_tao[0],
                              self.signal_generator.fn2d_tao[1])
        self.draw_function_2d(GraphType.FUNCTION_DOPPLER,
                              self.signal_generator.fn2d_doppler[0],
                              self.signal_generator.fn2d_doppler[1])
        # Печать результатов
        print("\nКритерий выраженности главного максимума:", self.signal_generator.criterion)
        print("Временная задержка из функции неопределенности, мс:", self.signal_generator.found_time_delay_f)
        print("Доплеровская частота из функции неопределенности, Гц:", self.signal_generator.found_doppler)

    def start_research_logic(self):
        """
        Обработчик запуска исследования.
        """
        # Запуск исследования
        try:
            average_count = int(self.average_count_edit.text())
        except ValueError:
            return

        x, y = calc_research_bad_alg(average_count, self.signal_generator)
        self.draw_criterion_research(x, y)

    def sr_change_logic(self):
        """
        Обработка события изменения значения в поле "Частота дискретизации".
        """
        if self.sampling_rate_edit.text().isdigit():
            self.signal_generator.sampling_rate = float(self.sampling_rate_edit.text())

    def bits_count_change_logic(self):
        """
        Обработка события изменения значения в поле "Количество информационных бит".
        """
        if self.bits_count_edit.text().isdigit():
            self.signal_generator.bits_count = int(self.bits_count_edit.text())

    def bits_per_second_change_logic(self):
        """
        Обработка события изменения значения в поле "Скорость передачи данных".
        """
        if self.bits_per_second_edit.text().isdigit():
            self.signal_generator.bits_per_second = float(self.bits_per_second_edit.text())

    def signal_freq_change_logic(self):
        """
        Обработка события изменения значения в поле "Несущая частота".
        """
        if self.signal_freq_edit.text().isdigit():
            self.signal_generator.signal_freq = float(self.signal_freq_edit.text())

    def time_delay_change_logic(self):
        """
        Обработка события изменения значения в поле "Временная задержка, мс".
        """
        if self.time_delay_edit.text().isdigit():
            self.signal_generator.time_delay = float(self.time_delay_edit.text())

    def snr_change_logic(self):
        """
        Обработка события изменения значения в поле "ОСШ".
        """
        try:
            self.signal_generator.snr = float(self.snr_edit.text())
        except ValueError:
            pass

    def doppler_change_logic(self):
        """
        Обработка события изменения значения в поле "Частота Доплера".
        """
        try:
            self.signal_generator.doppler_effect = float(self.doppler_edit.text())
        except ValueError:
            pass

    def restore_or_maximized(self):
        """
        Логика сворачивания и разворачивания окна.
        """
        current_geometry = self.geometry()
        if current_geometry.width() == self.full_screen_geometry.width() and \
                current_geometry.height() == self.full_screen_geometry.height():
            new_geometry = self.last_geometry
        else:
            new_geometry = self.full_screen_geometry
            self.last_geometry = current_geometry

        self.animation_geometry.setDuration(DURATION_MAXIMIZED)
        self.animation_geometry.setStartValue(current_geometry)
        self.animation_geometry.setEndValue(new_geometry)
        self.animation_geometry.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuart)
        self.animation_geometry.start()

    def mousePressEvent(self, event):
        """
        Получение координат курсора при клике.
        """
        self.click_position = event.globalPos()

    def move_window(self, e):
        """
        Логика перетаскивания окна приложения.
        """
        if not self.isMaximized():
            if e.buttons() == QtCore.Qt.MouseButton.LeftButton:
                self.move(self.pos() + e.globalPos() - self.click_position)
                self.click_position = e.globalPos()
                e.accept()

    def slide_left_menu(self):
        """
        Логика работы бокового меню.
        """
        width = self.side_menu_container.width()
        if width == MIN_WIDTH:
            new_width = MAX_WIDTH
            self.side_menu_button.setIcon(QtGui.QIcon(HIDE_MENU_ICON))
        else:
            new_width = MIN_WIDTH
            self.side_menu_button.setIcon(QtGui.QIcon(OPEN_MENU_ICON))

        self.animation_menu.setDuration(DURATION_SIDE_MENU)
        self.animation_menu.setStartValue(width)
        self.animation_menu.setEndValue(new_width)
        self.animation_menu.setEasingCurve(QtCore.QEasingCurve.Type.InOutQuad)
        self.animation_menu.start()
