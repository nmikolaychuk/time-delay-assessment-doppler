import random
import numpy as np

from defaults import *
from enums import *


class SignalGenerator:
    """
    Объект для генерации опорного сигнала
    """
    def __init__(self, s_r=DEFAULT_SAMPLING_RATE, s_freq=DEFAULT_SIGNAL_FREQ,
                 b_count=DEFAULT_BITS_COUNT, bps=DEFAULT_BITS_PER_SECOND,
                 t_delay=DEFAULT_TIME_DELAY, snr=DEFAULT_SNR, e_doppler=DEFAULT_DOPPLER):

        # Параметры сигнала
        self.sampling_rate = float(s_r)
        self.signal_freq = float(s_freq)
        self.bits_count = int(b_count)
        self.bits_per_second = float(bps)
        self.time_delay = int(t_delay)
        self.snr = float(snr)
        self.doppler_effect = float(e_doppler)
        self.signal_phase = 0.
        self.found_time_delay = 0

        # Буферы для хранения информационных бит
        self.reference_bits = []
        self.research_bits = []

        # Буферы для хранения I и Q компонент
        self.reference_i = []
        self.reference_q = []
        self.research_i = []
        self.research_q = []

        # Буферы для хранения модулированных сигналов
        self.reference_mod = []
        self.research_mod = []

        # Буфер для хранения взаимной корреляционной функции
        self.correlation = []

        # Буфер для хранения критерия выраженности главного максимума
        self.criterion = 0

        # Буфер для хранения взаимной функции неопределенности
        self.fn3d = []
        self.tao_list = []
        self.doppler_list = []
        self.fn2d_tao = []
        self.fn2d_doppler = []
        self.found_time_delay_f = 0
        self.found_doppler = 0

    @staticmethod
    def _generate_bits(bits_count):
        """
        Формирование случайной битовой информационной последовательности.
        """
        bits = []
        for i in range(int(bits_count)):
            x = random.randint(0, 1)
            bits.append(x)
        return bits

    @staticmethod
    def _get_components(bits: list):
        """
        Получить I и Q компоненты.
        """
        if len(bits) % 2 != 0:
            bits.append(0)

        i_component = []
        q_component = []
        for i in range(len(bits)):
            if i % 2 == 0:
                i_component.append(bits[i])
                i_component.append(bits[i])
            else:
                q_component.append(bits[i])
                q_component.append(bits[i])
        return i_component, q_component

    def _generate_info_bits(self):
        """
        Генерация информационных битов для эталонного и исследуемого сигналов.
        """
        research_bits_count = self.bits_count * 3
        self.research_bits = self._generate_bits(research_bits_count)
        self.reference_bits = self._generate_bits(self.bits_count)

    def _get_signal_parameters(self, bits_count):
        """
        Рассчитать параметры сигнала.
        """
        # Определение типа сигнала
        signal_type = SignalType.REFERENCE if bits_count == self.bits_count else SignalType.RESEARCH
        # Длительность одного бита
        bit_time = 1. / self.bits_per_second
        # Длительность сигнала
        signal_duration = bit_time * bits_count
        # Частота опорного сигнала
        w = 2. * np.pi * self.signal_freq
        # Количество отсчётов сигнала
        n = self.sampling_rate * signal_duration
        # Шаг времени
        timestep = signal_duration / n
        # Заполнение словаря с параметрами
        params = {"bit_time": bit_time,
                  "signal_duration": signal_duration,
                  "freq": w,
                  "timestep": timestep,
                  "signal_type": signal_type}
        return params

    def _calc_phase_modulation(self, params: dict):
        """
        Построить фазово-манипулированный сигнал.
        """
        # Получение параметров сигнала
        x, y = [], []
        # Временная задержка, сек
        td_sec = self.time_delay / 1000
        # Индекс массива при начале вставки
        add_idx = int(td_sec / params["bit_time"])
        for t in np.arange(0, params["signal_duration"], params["timestep"]):
            # Получение текущего бита
            bit_index = int(t / params["bit_time"])

            ph_i = 0
            ph_q = 0
            if params["signal_type"] == SignalType.REFERENCE:
                # Обработка фазовой манипуляции
                ph_i = (3. * np.pi) / 4. if self.reference_i[bit_index] == 0 else (7. * np.pi) / 4.
                ph_q = (3. * np.pi) / 4. if self.reference_q[bit_index] == 0 else (7. * np.pi) / 4.
            elif params["signal_type"] == SignalType.RESEARCH:
                # Вставка эталонного сигнала
                if t >= td_sec and (bit_index - add_idx) < len(self.reference_i):
                    # Обработка фазовой манипуляции
                    ph_i = (3. * np.pi) / 4. if self.reference_i[bit_index - add_idx] == 0 else (7. * np.pi) / 4.
                    ph_q = (3. * np.pi) / 4. if self.reference_q[bit_index - add_idx] == 0 else (7. * np.pi) / 4.
                else:
                    ph_i = (3. * np.pi) / 4. if self.research_i[bit_index] == 0 else (7. * np.pi) / 4.
                    ph_q = (3. * np.pi) / 4. if self.research_q[bit_index] == 0 else (7. * np.pi) / 4.

            # Заполнение списка отсчетов\значений
            value = complex(np.cos(params["freq"] * t + ph_i), np.cos(params["freq"] * t + ph_q))
            if params["signal_type"] == SignalType.RESEARCH:
                # Добавление доплеровского сдвига
                arg = self.doppler_effect * t * 2. * np.pi
                value *= complex(np.cos(arg), np.sin(arg))

            x.append(t)
            y.append(value)

        return [x, y]

    def calculate(self):
        """
        Произвести расчёт и получить графики.
        """
        # Генерация информационных битов
        self._generate_info_bits()
        # Получение I и Q компонент
        self.reference_i, self.reference_q = self._get_components(self.reference_bits)
        self.research_i, self.research_q = self._get_components(self.research_bits)
        # Модуляция
        self.reference_mod = self._calc_phase_modulation(self._get_signal_parameters(len(self.reference_i)))
        self.research_mod = self._calc_phase_modulation(self._get_signal_parameters(len(self.research_i)))
        # Добавление шума
        self.reference_mod = self._get_noise_parts(self.reference_mod)
        self.research_mod = self._get_noise_parts(self.research_mod)
        # Корреляция
        self.correlation = self._get_correlation()
        # Оценка временной задержки
        self.found_time_delay = self._find_correlation_max()
        # Вычисление критерия выраженности главного максимума
        self.criterion = self._calc_criterion()
        # Вычисление взаимной функции неопределенности
        self.fn3d = self._calc_3d_function()
        self._calc_2d_function()

    def _get_noise_parts(self, signal: list):
        """
        Наложить шум на комплексную огибающую.
        """
        r_part = self._get_complex_part(signal, ComplexPart.REAL)
        r_part = self._generate_noise(r_part)
        i_part = self._get_complex_part(signal, ComplexPart.IMAGE)
        i_part = self._generate_noise(i_part)
        return self._concat_complex_part(r_part, i_part)

    def _generate_noise(self, signal: list):
        """
        Генерация шума для сигнала
        """
        if not signal:
            return

        # Расчет энергии шума
        signal_energy = self._calc_signal_energy(signal)
        noise_energy = signal_energy / (10 ** (self.snr / 10))

        # Случайная шумовая добавка к каждому отсчету
        noise = []
        random_energy = 0.
        for i in range(len(signal[1])):
            random_value = self._get_random_value()
            noise.append(random_value)
            random_energy += random_value ** 2

        # Зашумленный сигнал
        alpha = np.sqrt(noise_energy / random_energy)
        noise_signal = []
        for i in range(len(signal[1])):
            noise_signal.append(signal[1][i] + alpha * noise[i])

        return [signal[0], noise_signal]

    @staticmethod
    def _calc_signal_energy(signal: list):
        """
        Расчет энергии сигнала
        """
        energy = 0.
        for i in range(len(signal[1])):
            energy += signal[1][i] ** 2
        return energy

    @staticmethod
    def _get_random_value():
        """
        Рандомизация чисел для шума
        """
        av = 20
        value = 0.
        for i in range(av):
            value += random.uniform(-1, 1)
        return value / av

    @staticmethod
    def _get_complex_part(signal: list, part: ComplexPart):
        """
        Получение синфазного/квадратурного сигнала.
        """
        x = signal[0]
        y = []
        if part == ComplexPart.REAL:
            y = [v.real for v in signal[1]]
        elif part == ComplexPart.IMAGE:
            y = [v.imag for v in signal[1]]
        return [x, y]

    @staticmethod
    def _concat_complex_part(real_part: list, image_part: list):
        """
        Получить комплексную огибающую по компонентам.
        """
        x = real_part[0]
        y = []
        for i in range(len(real_part[1])):
            y.append(complex(real_part[1][i], image_part[1][i]))
        return [x, y]

    def _get_correlation(self, is_abs: bool = True):
        """
        Расчет взаимной корреляционной функции опорного и исследуемого сигналов.
        """
        research = np.array(self.research_mod[1])
        modulate = np.array(self.reference_mod[1])
        y = np.correlate(research, modulate, 'valid').tolist()
        if is_abs:
            y = np.abs(y)
        y = y / np.max(y)
        x = self.research_mod[0][:len(y)]
        return [x, y]

    def _find_correlation_max(self):
        """
        Нахождение максимума корреляционной функции.
        """
        max_element_idx = np.argmax(self.correlation[1])
        return self.correlation[0][max_element_idx] * 1000

    def _calc_criterion(self):
        """
        Нахождение критерия выраженности главного максимума.
        """
        # Нахождение значения главного максимума
        max_value_idx = np.argmax(self.correlation[1])
        # Вычисление среднеквадратичного отклонения
        return self.correlation[1][max_value_idx] / np.std(self.correlation[1])

    def _calc_3d_function(self):
        """
        Вычисление взаимной функции неопределенности.
        """
        # Вычисление корреляции
        research = np.array(self.research_mod[1])
        modulate = np.conj(np.array(self.reference_mod[1]))
        # Вычисление диапазона времени
        from_time = 0
        to_time = self.research_mod[0][-len(self.reference_mod[0])]
        step_time = self.reference_mod[0][1] - self.reference_mod[0][0]
        # Значения частоты
        y = np.fft.fftfreq(modulate.size, d=step_time)
        # Значения времени, значения функции неопределенности
        x, z = [], []
        for t in np.arange(from_time, to_time, step_time):
            # Вычисление индекса
            idx = int(t / step_time)
            # Вычисление корреляции
            mul = np.multiply(modulate, research[idx:idx+modulate.shape[0]])
            # Вычисление Фурье
            fourier = np.fft.fft(mul).tolist()
            x.append(t)
            z.append(np.abs(fourier))

        # Сохранение значений на осях
        self.tao_list = x
        self.doppler_list = y.tolist()
        # Преобразование значений на осях к 2d array
        x, y = np.meshgrid(np.array(x), y)
        return [x, y, np.stack(z, axis=1)]

    def _calc_2d_function(self):
        """
        Вычисление взаимной функции неопределенности.
        """
        self.fn2d_tao = [self.tao_list, np.amax(self.fn3d[2], axis=0).tolist()]
        doppler_y_values = np.amax(self.fn3d[2], axis=1).tolist()
        doppler_x, doppler_y = zip(*sorted(zip(self.doppler_list, doppler_y_values)))
        self.fn2d_doppler = [doppler_x, doppler_y]
        self.found_doppler = doppler_x[np.argmax(doppler_y)]
        self.found_time_delay_f = self.tao_list[np.argmax(self.fn2d_tao[1])] * 1000
