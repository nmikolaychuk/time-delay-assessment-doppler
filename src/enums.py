from enum import Enum


class GraphType(Enum):
    """
    Типы графиков для отрисовки
    """
    REFERENCE = 0
    RESEARCH = 1
    CORRELATION = 2
    FUNCTION_TAO = 3
    FUNCTION_DOPPLER = 4


class ComplexPart(Enum):
    """
    Компоненты сигнала
    """
    REAL = 0
    IMAGE = 1


class SignalType(Enum):
    """
    Типы сигналов для модуляции
    """
    REFERENCE = 0
    RESEARCH = 1


class ModulationType(Enum):
    """
    Типы модуляции.
    """
    AM = 0
    FM = 1
    PM = 2
