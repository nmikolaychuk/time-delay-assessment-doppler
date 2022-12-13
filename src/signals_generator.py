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

    def _get_noise_parts(self, signal: list, signal_type: SignalType):
        """
        Наложить шум на комплексную огибающую.
        """
        r_part = self._get_complex_part(signal, ComplexPart.REAL)
        r_part = self._generate_noise(signal_type, r_part)
        i_part = self._get_complex_part(signal, ComplexPart.IMAGE)
        i_part = self._generate_noise(signal_type, i_part)
        return self._concat_complex_part(r_part, i_part)

    def _generate_noise(self, signal_type: SignalType, signal: list):
        """
        Генерация шума для сигнала
        """
        snr = None
        if signal_type == SignalType.REFERENCE:
            snr = 10
        elif signal_type == SignalType.RESEARCH:
            snr = self.snr

        if not signal:
            return

        # Расчет энергии шума
        signal_energy = self._calc_signal_energy(signal)
        noise_energy = signal_energy / (10 ** (snr / 10))

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

    @staticmethod
    def _get_correlation(modulated: list, researched: list):
        """
        Расчет взаимной корреляционной функции опорного и исследуемого сигналов.
        """
        if not modulated or not researched:
            return

        research = np.array(researched[1])
        modulate = np.array(modulated[1])
        y = np.abs(np.correlate(research, modulate, 'valid').tolist())
        y = y / np.max(y)
        x = researched[0][:len(y)]
        return [x, y]

    @staticmethod
    def _find_correlation_max(correlation: list):
        """
        Нахождение максимума корреляционной функции
        """
        if not correlation:
            return

        max_element_idx = np.argmax(correlation[1])
        return correlation[0][max_element_idx] * 1000
