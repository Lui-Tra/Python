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

    def associative_law(self):
        return self

    def absorption(self):
        return self

    def idempotence(self):
        return self

    def trivial_simplification(self):
        return self

    def dominance(self):
        return self

    def identity(self):
        return self

    def not_operator_simplify(self):
        return self

    def replace_with_and_or(self):
        return self

    def smart_expand(self):
        return self

    def to_nand(self):
        return self

    def to_nor(self):
        pass

    def __repr__(self):
        return str(self)
