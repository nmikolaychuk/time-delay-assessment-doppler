from signals_generator import SignalGenerator
from defaults import *
from enums import *


def calc_research(average_count: int, signal_generator: SignalGenerator,
                  from_noise: int = 10, to_noise: int = -11, step_noise: int = -1):
    # Длительность бита
    bit_time = 1. / float(DEFAULT_BITS_PER_SECOND)
    # Доверительный интервал
    min_t = float(signal_generator.time_delay) - 0.5 * bit_time
    max_t = float(signal_generator.time_delay) + 0.5 * bit_time
    # Изменение уровня шума
    x_am, y_am, errors_am = [], [], []
    x_fm, y_fm, errors_fm = [], [], []
    x_pm, y_pm, errors_pm = [], [], []
    for snr in range(from_noise, to_noise, step_noise):
        print(f"Запускается расчет исследования при {snr} дБ...")
        # Обновление уровня шума
        signal_generator.snr = float(snr)
        # Количество положительных исходов
        good_count_am = 0
        good_count_fm = 0
        good_count_pm = 0
        # Цикл для усреднений
        for avg in range(average_count):
            # Модулированные сигналы
            modulate_am = signal_generator.calc_modulated_signal(SignalType.GENERAL, ModulationType.AM)
            modulate_fm = signal_generator.calc_modulated_signal(SignalType.GENERAL, ModulationType.FM)
            modulate_pm = signal_generator.calc_modulated_signal(SignalType.GENERAL, ModulationType.PM)
            # Исследуемые сигналы
            research_am = signal_generator.calc_modulated_signal(SignalType.RESEARCH, ModulationType.AM)
            research_fm = signal_generator.calc_modulated_signal(SignalType.RESEARCH, ModulationType.FM)
            research_pm = signal_generator.calc_modulated_signal(SignalType.RESEARCH, ModulationType.PM)
            # Вставка модулированных сигналов в исследуемые
            researched_am = signal_generator.calc_research_signal(modulate_am, research_am)
            researched_fm = signal_generator.calc_research_signal(modulate_fm, research_fm)
            researched_pm = signal_generator.calc_research_signal(modulate_pm, research_pm)
            # Добавление шума
            modulate_n_am = signal_generator.generate_noise(SignalType.GENERAL, modulate_am)
            modulate_n_fm = signal_generator.generate_noise(SignalType.GENERAL, modulate_fm)
            modulate_n_pm = signal_generator.generate_noise(SignalType.GENERAL, modulate_pm)
            researche_n_am = signal_generator.generate_noise(SignalType.RESEARCH, researched_am)
            researche_n_fm = signal_generator.generate_noise(SignalType.RESEARCH, researched_fm)
            researche_n_pm = signal_generator.generate_noise(SignalType.RESEARCH, researched_pm)
            # Расчёт корреляции
            correlation_am = signal_generator.get_correlation(modulate_n_am, researche_n_am)
            correlation_fm = signal_generator.get_correlation(modulate_n_fm, researche_n_fm)
            correlation_pm = signal_generator.get_correlation(modulate_n_pm, researche_n_pm)

            # Нахождение временной задержки
            time_delay_am = signal_generator.find_correlation_max(correlation_am)
            time_delay_fm = signal_generator.find_correlation_max(correlation_fm)
            time_delay_pm = signal_generator.find_correlation_max(correlation_pm)

            if min_t <= time_delay_am <= max_t:
                good_count_am += 1

            if min_t <= time_delay_fm <= max_t:
                good_count_fm += 1

            if min_t <= time_delay_pm <= max_t:
                good_count_pm += 1

        x_am.append(snr)
        y_am.append(good_count_am / average_count)
        errors_am.append(0.5 * bit_time)

        x_fm.append(snr)
        y_fm.append(good_count_fm / average_count)
        errors_fm.append(0.5 * bit_time)

        x_pm.append(snr)
        y_pm.append(good_count_pm / average_count)
        errors_pm.append(0.5 * bit_time)

    return x_am, y_am, errors_am, x_fm, y_fm, errors_fm, x_pm, y_pm, errors_pm
