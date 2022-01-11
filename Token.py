from abc import ABC
from abc import abstractmethod

from constants import center


class Token(ABC):
    def __init__(self):
        self.value = None

    @abstractmethod
    def calculate_value(self):
        pass

    @abstractmethod
    def get_truth_table_header(self):
        pass

    @abstractmethod
    def get_truth_table_entry(self):
        pass

    @abstractmethod
    def nnf(self):
        pass

    def __repr__(self):
        return str(self)
