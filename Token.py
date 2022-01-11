from abc import ABC
from abc import abstractmethod


class Token(ABC):
    def __init__(self):
        self.current_value = None

    @abstractmethod
    def nnf(self):
        pass

    @abstractmethod
    def calculate_value(self):
        pass

    def __repr__(self):
        return str(self)
