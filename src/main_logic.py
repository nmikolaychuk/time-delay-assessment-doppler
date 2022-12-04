from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, QtCore, QtGui

from main_interface import Ui_MainWindow
from mpl_widget import MplGraphicsModulated, MplGraphicsResearch
from signals_generator import SignalGenerator
from research_logic import calc_research
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

    def draw(self, graph_type: GraphType, x: list, y: list):
        """
        Нарисовать график.
        """
        if graph_type == GraphType.MODULATED:
            self.graphics.clear_plot_ax1()
            self.graphics.plot_graph_ax1(x, y)
        elif graph_type == GraphType.RESEARCH:
            self.graphics.clear_plot_ax2()
            self.graphics.plot_graph_ax2(x, y)
        elif graph_type == GraphType.CORRELATION:
            self.graphics.clear_plot_ax3()
            self.graphics.plot_graph_ax3(x, y)

        self.graphics.draw()
        self.graphics.flush_events()

    def draw_ber_of_snr(self, x_am: list, y_am: list, err_am: list,
                        x_fm: list, y_fm: list, err_fm: list,
                        x_pm: list, y_pm: list, err_pm: list):
        """
        Отобразить график исследования.
        """
        self.research_graphics.clear_plot()
        self.research_graphics.plot_graph(x_am, y_am, err_am, x_fm, y_fm, err_fm, x_pm, y_pm, err_pm)
        self.research_graphics.draw()
        self.research_graphics.flush_events()

    def draw_main_page_graphics(self):
        """
        Отрисовка графиков на главной странице.
        """
        # Пересчет параметров
        self.signal_generator.recalc_parameters()
        if self.am_manipulation_radio.isChecked():
            x, y = self.signal_generator.calc_modulated_signal(SignalType.GENERAL, ModulationType.AM)
            xr, yr = self.signal_generator.calc_modulated_signal(SignalType.RESEARCH, ModulationType.AM)
            self.signal_generator.modulated_signal = [x, y]
            self.signal_generator.research_signal = [xr, yr]
        elif self.mchm_manipulation_radio.isChecked():
            x, y = self.signal_generator.calc_modulated_signal(SignalType.GENERAL, ModulationType.FM)
            xr, yr = self.signal_generator.calc_modulated_signal(SignalType.RESEARCH, ModulationType.FM)
            self.signal_generator.modulated_signal = [x, y]
            self.signal_generator.research_signal = [xr, yr]
        elif self.fm2_manipulation_radio.isChecked():
            x, y = self.signal_generator.calc_modulated_signal(SignalType.GENERAL, ModulationType.PM)
            xr, yr = self.signal_generator.calc_modulated_signal(SignalType.RESEARCH, ModulationType.PM)
            self.signal_generator.modulated_signal = [x, y]
            self.signal_generator.research_signal = [xr, yr]

        # Получение бит для отрисовки
        bits = self.signal_generator.get_bits_to_plot()

        # Вставка маленького сигнала в большой
        research = self.signal_generator.calc_research_signal(self.signal_generator.modulated_signal,
                                                              self.signal_generator.research_signal)
        self.signal_generator.research_signal = research

        # Добавление шума
        modulated = self.signal_generator.generate_noise(SignalType.GENERAL,
                                                         self.signal_generator.modulated_signal)
        self.signal_generator.modulated_signal = modulated
        researched = self.signal_generator.generate_noise(SignalType.RESEARCH,
                                                          self.signal_generator.research_signal)
        self.signal_generator.research_signal = researched

        # Расчет взаимной корреляционной функции
        correlation = self.signal_generator.get_correlation(self.signal_generator.modulated_signal,
                                                            self.signal_generator.research_signal)
        self.signal_generator.correlation_signal = correlation

        # Оценка временной задержки
        time_delay = self.signal_generator.find_correlation_max(self.signal_generator.correlation_signal)
        self.time_delay_assessment_edit.setText(str(time_delay) + " мс")

        # Отрисовка
        if self.signal_generator.modulated_signal and \
            self.signal_generator.research_signal and \
                self.signal_generator.correlation_signal and bits:
            # Генерация исследуемого сигнала
            self.draw(GraphType.MODULATED,
                      self.signal_generator.modulated_signal[0],
                      self.signal_generator.modulated_signal[1])
            self.draw(GraphType.RESEARCH,
                      self.signal_generator.research_signal[0],
                      self.signal_generator.research_signal[1])
            self.draw(GraphType.CORRELATION,
                      self.signal_generator.correlation_signal[0],
                      self.signal_generator.correlation_signal[1])
            self.draw(GraphType.BITS,
                      bits[0],
                      bits[1])

    def start_research_logic(self):
        """
        Обработчик запуска исследования.
        """
        # Запуск исследования
        try:
            average_count = int(self.average_count_edit.text())
        except ValueError:
            return

        x_am, y_am, err_am, x_fm, y_fm, err_fm, x_pm, y_pm, err_pm = calc_research(average_count, self.signal_generator)
        self.draw_ber_of_snr(x_am, y_am, err_am, x_fm, y_fm, err_fm, x_pm, y_pm, err_pm)

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
        Обработка события изменения значения в поле "Временная задержка".
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
