import numpy as np

from signals_generator import SignalGenerator
from enums import ModulationType

MOD_TYPE = ModulationType.FM


def calc_research_bad_alg(average_count: int, signal_generator: SignalGenerator,
                          from_doppler: float = 0., to_doppler: float = 3., step_doppler: float = 0.01):
    """
    Исследование устойчивости алгоритма оценки взаимной временной задержки
    сигналов на основе метода максимального правдоподобия в зависимости от
    доплеровского смещения.
    """
    x, y = [], []
    for dpl in np.arange(from_doppler, to_doppler, step_doppler):
        print(f"Запускается расчет исследования при {dpl} Гц...")
        # Обновление доплеровского смещения
        signal_generator.doppler_effect = dpl
        # Переменная для усреднения
        avg_criterion = 0
        # Цикл для усреднений
        for avg in range(average_count):
            # Вычисление задержки
            signal_generator.calculate(MOD_TYPE)
            avg_criterion += signal_generator.criterion
        # Усредненный критерий
        avg_criterion /= average_count
        x.append(dpl)
        y.append(avg_criterion)
    return [x, y]
