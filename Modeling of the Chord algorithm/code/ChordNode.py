from __future__ import annotations

import random
from typing import List, Optional

from tabulate import tabulate

from Finger import Finger


class ChordNode:
    """Реализация узла в алгоритме хорд."""

    id: int
    Finger: List[Finger]

    def __init__(self, n: int, m: int):
        """Инициализация узла в алгоритме хорд.

        n: количество узлов в системе
        m: количество бит, используемых для генерации идентификаторов
        """
        self.id = n
        self.Finger = [Finger(n, m, i, self) for i in range(0, m)]
        self.__predecessor = self

    def get_successor(self) -> ChordNode:
        """Возвращает successor."""
        return self.Finger[0].node

    def set_successor(self, node: ChordNode):
        """Присваивает successor."""
        self.Finger[0].node = node

    def get_predecessor(self) -> ChordNode:
        """Возвращает predecessor."""
        return self.__predecessor

    def set_predecessor(self, node: Optional[ChordNode]):
        """Присваивает predecessor."""
        self.__predecessor = node

    def find_successor(self, node_id: int):
        """Поиск successor по id."""
        node = self.find_predecessor(node_id)
        return node.get_successor()

    def find_predecessor(self, node_id: int):
        """Поиск predecessor по id."""
        node = self
        while not (self.__id_in_interval(node_id, node.id, node.get_successor().id)
                   or node_id == node.get_successor().id):
            node = node.closest_preceding_finger(node_id)
        return node

    def closest_preceding_finger(self, node_id: int):
        """Поиск preceding finger."""
        m = len(self.Finger)
        for i in range(m - 1, -1, -1):
            node: ChordNode = self.Finger[i].node
            if self.__id_in_interval(node.id, self.id, node_id):
                return node
        return self

    def join(self, node: Optional[ChordNode]) -> None:
        """Добавление нового узла."""
        if node:
            self.init_finger_table(node)
            self.update_others()
        else:
            for i in range(len(self.Finger)):
                self.Finger[i].node = self
            self.set_predecessor(self)

    def init_finger_table(self, node: ChordNode) -> None:
        """Инициализация таблицы finger."""
        self.Finger[0].node = node.find_predecessor(self.Finger[0].interval[0])
        successor = self.get_successor()
        self.set_predecessor(successor.get_predecessor())
        successor.set_predecessor(self)
        for i in range(0, len(self.Finger)):
            if self.__id_in_interval(self.Finger[i + 1].interval[0], self.id, self.Finger[i].node.id) \
                    or self.id == self.Finger[i + 1].interval[0]:
                self.Finger[i + 1].node = self.Finger[i].node
            else:
                self.Finger[i + 1].node = node.find_successor(self.Finger[i + 1].interval[0])

    def update_others(self) -> None:
        """Обновление узло."""
        for i in range(0, len(self.Finger)):
            p = self.find_predecessor(node_id=(self.id - 2 ** i) % 2 ** len(self.Finger))
            p.update_finger_table(self, i)

    def update_finger_table(self, s: ChordNode, i: int) -> None:
        """Обновление таблицы информации об узлах."""
        if s.id == self.id or self.__id_in_interval(s.id, self.id, self.Finger[i].node.id):
            self.Finger[i].node = s
            p = self.get_predecessor()
            if p:
                p.update_finger_table(s, i)

    def join_to_node(self, node: Optional[ChordNode]) -> None:
        if node:
            self.set_predecessor(None)
            self.set_successor(node.find_successor(self.id))
        else:
            for finger in self.Finger:
                finger.node = self
            self.set_predecessor(self)

    def stabilize(self) -> None:
        """Стабилизация системы."""
        x = self.get_successor().get_predecessor()
        if self.__id_in_interval(x.id, self.id, self.get_successor().id):
            self.set_successor(x)
        self.get_successor().notify(self)

    def notify(self, node: ChordNode) -> None:
        """Проверка на predecessor."""
        if self.get_predecessor() is None \
                or self.__id_in_interval(node.id, self.get_predecessor().id, self.id):
            self.set_predecessor(node)

    def fix_fingers(self) -> None:
        """Периодическое обновление таблицы finger."""
        i = random.randrange(len(self.Finger))
        self.Finger[i].node = self.find_successor(self.Finger[i].interval[0])

    def __id_in_interval(self, node_id: int, start: int, end: int) -> bool:
        """Вспомогательная функция для проверки вхождения узла с id в
        интервале.

        [start, end).
        """
        m = len(self.Finger)
        _node_id = node_id
        _start = start
        _end = end
        if _start >= _end:
            _end += 2 ** m
            if _start > node_id:
                _node_id += 2 ** m
        return _start < _node_id < _end

    def remove(self) -> None:
        if self.get_predecessor():
            self.get_predecessor().set_successor(self.get_successor())
        self.get_successor().set_predecessor(self.get_predecessor())

        for i in range(len(self.Finger)):
            j = self.id - 2 ** i
            p = self.find_predecessor(j)
            p.update_finger_table(self.get_successor(), i)

    def __str__(self):
        """Визуализация таблицы."""
        finger_table = [*[[finger.interval, finger.node.id] for finger in self.Finger]]

        return f"\nID: {self.id}\nFinger Table:\n{tabulate(finger_table, headers=['Interval', 'Node'], tablefmt='pretty')}"
