from abc import ABC, abstractmethod
from src.domain.hospital import Hospital
from src.domain.patient import Patient


class PriorityPolicy(ABC):

    @abstractmethod
    def order_patients(
        self, patients: list[Patient], hospital: Hospital, arrivals: list[Patient] = []
    ) -> list[Patient]:
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def sig(self):
        return "None"
