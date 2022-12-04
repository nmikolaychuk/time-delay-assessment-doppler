from enum import Enum


class GraphType(Enum):
    """
    Типы графиков для отрисовки
    """
    MODULATED = 0
    RESEARCH = 1
    CORRELATION = 2
    BITS = 3
    BER_OF_SNR = 4


class SignalType(Enum):
    """
    Типы сигналов для модуляции
    """
    GENERAL = 0
    RESEARCH = 1


class ModulationType(Enum):
    """
    Типы модуляции.
    """
    AM = 0
    FM = 1
    PM = 2
