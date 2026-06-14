from src.domain.hospital import Hospital
from src.domain.patient import Patient
from src.policies.base_policy import PriorityPolicy


class SeverityPolicy(PriorityPolicy):

    def order_patients(
        self, patients: list[Patient], hospital: Hospital, arrivals: list[Patient] = []
    ) -> list[Patient]:
        patients += arrivals
        return sorted(patients, key=lambda p: p.health_level)

    def __repr__(self):
        return "Severity Policy"
