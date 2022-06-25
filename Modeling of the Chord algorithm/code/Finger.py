from __future__ import annotations

from typing import Tuple


def generate_start(n: int, m: int, i: int) -> int:
    """Функция, которая генерирует старотовое значение Finger."""
    return (n + 2 ** i) % 2 ** m


class Finger:
    """"Класс для хранения вспомогательной информации об узлах."""

    interval: Tuple[int, int]
    node = None

    def __init__(self, n: int, m: int, i: int, node):
        """Инициализациия ифнормации об узлах.

        n: количество узлов
        m: количество бит, используемых для генерации идентификаторов
        i: индекс входа
        node: узел
        """
        self.__start = generate_start(n, m, i)
        self.__end = generate_start(n, m, i + 1)
        self.interval = (self.__start, self.__end)
        self.node = node
