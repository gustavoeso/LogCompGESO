from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self, value=None):
        self.value = value
        self.children = []

    @abstractmethod
    def Evaluate(self, symbol_table):
        pass