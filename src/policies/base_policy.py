from abc import ABC, abstractmethod
from src.domain.hospital import Hospital
from src.domain.patient import Patient


class PriorityPolicy(ABC):

    @abstractmethod
    def order_patients(
        self, patients: list[Patient], hospital: Hospital
    ) -> list[Patient]:
        pass
