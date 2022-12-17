from PyQt5 import QtWidgets

from matplotlib import cm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MplGraphics2dFunction(FigureCanvas):
    """
    Функция отрисовки
    """
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi, facecolor=(.94, .94, .94, 0.), figsize=(4, 3))

        # Добавление области графа
        self.fig.set_constrained_layout(True)
        axd = self.fig.subplot_mosaic(
            """
            AABB
            """)

        self.ax1 = axd['A']
        self.ax2 = axd['B']
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
        self.ax1.grid(linestyle="dotted", alpha=0.65)
        self.ax1.set_xlabel('tao, сек')
        self.ax2.grid(linestyle="dotted", alpha=0.65)
        self.ax2.set_xlabel('doppler, Гц')

    def plot_graph_ax1(self, x_list: list, y_list: list):
        """
        Построение временного среза максимумов.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        self.ax1.plot(x_list, y_list, markersize=2, color='r')
        self.ax1.margins(y=0.8)

    def plot_graph_ax2(self, x_list: list, y_list: list):
        """
        Построение частотного среза максимумов.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        self.ax2.plot(x_list, y_list, markersize=2, color='g')
        self.ax2.margins(y=0.8)

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


class MplGraphics3dFunction(FigureCanvas):
    """
        Функция отрисовки
    """
    def __init__(self):
        plt.rcParams["figure.facecolor"] = (.94, .94, .94, 0.)
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d", "facecolor": ".9"})
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
        self.ax.set_title("Взаимная функция неопределенности")
        self.ax.grid(linestyle="dotted", alpha=0.65)
        self.ax.set_xlabel('tao, сек')
        self.ax.set_ylabel('doppler, Гц')
        self.ax.view_init(20, -45)

    def plot_graph(self, x, y, z):
        """
        Построение графика функции модулированного сигнала.
        """
        self.ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=2)

    def clear_plot(self):
        """
        Очистка области графика.
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
        self.ax.set_title("График устойчивости алгоритма в зависимости от доплеровского смещения")
        self.ax.grid(linestyle="dotted", alpha=0.65)

    def plot_graph(self, x: list, y: list):
        """
        Построение графика функции модулированного сигнала.
        """
        self.ax.plot(x, y, linestyle="-", markersize=2, color='r')

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
        self.fig.set_constrained_layout(True)
        axd = self.fig.subplot_mosaic(
            """
            AABB
            IIQQ
            CCCC
            """)

        self.ax1 = axd['A']
        self.ax2 = axd['B']
        self.ax3 = axd['I']
        self.ax4 = axd['Q']
        self.ax5 = axd['C']
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
        self.ax1.grid(linestyle="dotted", alpha=0.65)
        self.ax2.grid(linestyle="dotted", alpha=0.65)
        self.ax3.grid(linestyle="dotted", alpha=0.65)
        self.ax4.grid(linestyle="dotted", alpha=0.65)
        self.ax5.grid(linestyle="dotted", alpha=0.65)

    def plot_graph_ax1(self, x_list: list, y_list: list):
        """
        Построение синфазной компоненты эталонного сигнала.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        # Получение синфазных компонент.
        y = [v.real for v in y_list]

        self.ax1.plot(x_list, y, linestyle="-", markersize=2, color='r', label="I (эталонный сигнал)")
        self.ax1.legend(loc="upper right", framealpha=1.0)
        self.ax1.margins(y=0.8)

    def plot_graph_ax2(self, x_list: list, y_list: list):
        """
        Построение квадратурной компоненты эталонного сигнала.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        # Получение квадратурных компонент.
        y = [v.imag for v in y_list]

        self.ax2.plot(x_list, y, linestyle="-", markersize=2, color='g', label="Q (эталонный сигнал)")
        self.ax2.legend(loc="upper right", framealpha=1.0)
        self.ax2.margins(y=0.8)

    def plot_graph_ax3(self, x_list: list, y_list: list):
        """
        Построение синфазной компоненты исследуемого сигнала.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        # Получение синфазных компонент.
        y = [v.real for v in y_list]

        self.ax3.plot(x_list, y, linestyle="-", markersize=2, color='r', label="I (исследуемый сигнал)")
        self.ax3.legend(loc="upper right", framealpha=1.0)
        self.ax3.margins(y=0.8)

    def plot_graph_ax4(self, x_list: list, y_list: list):
        """
        Построение квадратурной компоненты исследуемого сигнала.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        # Получение синфазных компонент.
        y = [v.imag for v in y_list]

        self.ax4.plot(x_list, y, linestyle="-", markersize=2, color='g', label="Q (исследуемый сигнал)")
        self.ax4.legend(loc="upper right", framealpha=1.0)
        self.ax4.margins(y=0.8)

    def plot_graph_ax5(self, x_list: list, y_list: list):
        """
        Построение взаимной корреляционной функции эталонного и исследуемого сигналов.

        :param x_list: Список временный отсчётов.
        :param y_list: Список значений.
        :return: None.
        """
        self.ax5.plot(x_list, y_list, linestyle="-", markersize=2, color='indigo', label="Взаимная корреляционная функция")
        self.ax5.legend(loc="upper right", framealpha=1.0)
        self.ax5.margins(y=0.8)

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

    def clear_plot_ax4(self):
        """
        Очистка области графика.

        :return: None.
        """
        self.ax4.clear()
        self.add_text()

    def clear_plot_ax5(self):
        """
        Очистка области графика.

        :return: None.
        """
        self.ax5.clear()
        self.add_text()
