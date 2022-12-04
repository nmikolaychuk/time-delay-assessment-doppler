from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplGraphicsHelped(FigureCanvas):
    """
    Функция отрисовки
    """
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi, facecolor=(.94, .94, .94, 0.), figsize=(4, 3))

        # Добавление области графа
        self.ax = self.fig.add_subplot(111)
        self.add_text()

        # Инициализация
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Policy.Expanding,
                                   QtWidgets.QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)

    def add_text(self):
        """
        Инициализация графика.

        :return: None.
        """
        # Инициализация области графика модулированного сигнала
        self.ax.set_title("Последовательность информационных бит")
        self.ax.grid(linestyle="dotted", alpha=0.65)

    def plot_graph(self, x_list: list, y_list: list, label: str):
        """
        Построение графика функции модулированного сигнала.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :param label: Подпись графика.
        :return: None.
        """
        self.ax.plot(x_list, y_list, linestyle="-", markersize=2, color='r', label=label)
        self.ax.legend(loc="upper right", framealpha=1.0)
        self.ax.margins(y=0.8)

    def clear_plot(self):
        """
        Очистка области графика.

        :return: None.
        """
        self.ax.clear()
        self.add_text()


class MplGraphicsResearch(FigureCanvas):
    """
    Функция отрисовки
    """
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi, facecolor=(.94, .94, .94, 0.), figsize=(4, 3))

        # Добавление области графа
        self.ax = self.fig.add_subplot(111)
        self.add_text()

        # Инициализация
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Policy.Expanding,
                                   QtWidgets.QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)

    def add_text(self):
        """
        Инициализация графика.
        """
        # Инициализация области графика модулированного сигнала
        self.ax.set_title("График зависимости BER от SNR")
        self.ax.grid(linestyle="dotted", alpha=0.65)

    def plot_graph(self, x_am: list, y_am: list, errors_am: list,
                   x_fm: list, y_fm: list, errors_fm: list,
                   x_pm: list, y_pm: list, errors_pm: list):
        """
        Построение графика функции модулированного сигнала.
        """
        self.ax.errorbar(x_am, y_am, yerr=errors_am, fmt='o', linestyle='-', markersize=3, elinewidth=0.5,
                         ecolor='black', color='r', label="АМ", capsize=2, capthick=0.5)
        self.ax.errorbar(x_fm, y_fm, yerr=errors_fm, fmt='o', linestyle='-', markersize=3, elinewidth=0.5,
                         ecolor='black', color='g', label="ЧМ", capsize=2, capthick=0.5)
        self.ax.errorbar(x_pm, y_pm, yerr=errors_pm, fmt='o', linestyle='-', markersize=3, elinewidth=0.5,
                         ecolor='black', color='b', label="ФМ", capsize=2, capthick=0.5)

        self.ax.legend(loc="lower right", framealpha=1.0)

    def clear_plot(self):
        """
        Очистка области графика.
        """
        self.ax.clear()
        self.add_text()


class MplGraphicsModulated(FigureCanvas):
    """
    Функция отрисовки
    """
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi, facecolor=(.94, .94, .94, 0.), figsize=(4, 3))

        # Добавление области графа
        self.ax1 = self.fig.add_subplot(311)
        self.ax2 = self.fig.add_subplot(312)
        self.ax3 = self.fig.add_subplot(313)
        self.add_text()

        # Инициализация
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Policy.Expanding,
                                   QtWidgets.QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)

    def add_text(self):
        """
        Инициализация графика.

        :return: None.
        """
        # Инициализация области графика модулированного сигнала
        self.ax1.set_title("Смоделированные сигналы / оценка временной задержки")

        self.ax1.grid(linestyle="dotted", alpha=0.65)
        self.ax2.grid(linestyle="dotted", alpha=0.65)
        self.ax3.grid(linestyle="dotted", alpha=0.65)

    def plot_graph_ax1(self, x_list: list, y_list: list):
        """
        Построение графика функции модулированного сигнала.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        self.ax1.plot(x_list, y_list, linestyle="-", markersize=2, color='r', label="Манипулированный сигнал")
        self.ax1.legend(loc="upper right", framealpha=1.0)
        self.ax1.margins(y=0.8)

    def plot_graph_ax2(self, x_list: list, y_list: list):
        """
        Построение графика функции исследуемого сигнала.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        self.ax2.plot(x_list, y_list, linestyle="-", markersize=2, color='g', label="Исследуемый сигнал")
        self.ax2.legend(loc="upper right", framealpha=1.0)
        self.ax2.margins(y=0.8)

    def plot_graph_ax3(self, x_list: list, y_list: list):
        """
        Построение графика взаимной корреляционной функции.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        self.ax3.plot(x_list, y_list, linestyle="-", markersize=2, color='b', label="Взаимная корреляционная функция")
        self.ax3.legend(loc="upper right", framealpha=1.0)
        self.ax3.margins(y=0.8)

    def clear_plot_ax1(self):
        """
        Очистка области графика.

        :return: None.
        """
        self.ax1.clear()
        self.add_text()

    def clear_plot_ax2(self):
        """
        Очистка области графика.

        :return: None.
        """
        self.ax2.clear()
        self.add_text()

    def clear_plot_ax3(self):
        """
        Очистка области графика.

        :return: None.
        """
        self.ax3.clear()
        self.add_text()
