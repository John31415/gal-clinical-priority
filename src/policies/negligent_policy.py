from src.domain.hospital import Hospital
from src.domain.patient import Patient
from src.policies.base_policy import PriorityPolicy


class NegligentPolicy(PriorityPolicy):

    def order_patients(
        self, patients: list[Patient], hospital: Hospital, arrivals: list[Patient] = []
    ) -> list[Patient]:
        patients += arrivals
        return sorted(patients, key=lambda p: p.health_level, reverse=True)

    def __repr__(self):
        return "Negligent Policy"
