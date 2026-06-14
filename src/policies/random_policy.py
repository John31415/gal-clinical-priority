import random
from src.domain.hospital import Hospital
from src.domain.patient import Patient
from src.policies.base_policy import PriorityPolicy


class RandomPolicy(PriorityPolicy):

    def order_patients(
        self, patients: list[Patient], hospital: Hospital, arrivals: list[Patient] = []
    ) -> list[Patient]:
        patients += arrivals
        ordered = list(patients)
        random.shuffle(ordered)
        return ordered

    def __repr__(self):
        return "Random Policy"
