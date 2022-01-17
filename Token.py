from abc import ABC
from abc import abstractmethod


class Token(ABC):
    def __init__(self):
        self.value = None

    @abstractmethod
    def calculate_value(self):
        pass

    @abstractmethod
    def get_truth_table_header(self, depth):
        pass

    @abstractmethod
    def get_truth_table_entry(self, depth):
        pass

    @abstractmethod
    def nnf(self):
        pass

    @abstractmethod
    def simplify(self):
        pass

    def __repr__(self):
        return str(self)
