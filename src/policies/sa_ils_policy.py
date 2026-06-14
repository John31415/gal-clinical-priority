from src.policies.base_policy import PriorityPolicy
from src.policies.simulated_annealing_policy import SimAnnealPolicy
from src.policies.iterated_local_search_policy import ILSPolicy
from src.domain.hospital import Hospital
from src.domain.patient import Patient


class SAILSPolicy(PriorityPolicy):

    def order_patients(
        self, patients: list[Patient], hospital: Hospital, arrivals: list[Patient] = []
    ) -> list[Patient]:
        return SimAnnealPolicy().order_patients(
            patients=ILSPolicy().order_patients(
                patients=patients, hospital=hospital, arrivals=arrivals
            ),
            hospital=hospital,
        )

    def __repr__(self):
        return "Hybrid Policy: Simulated Annealing and Iterated Local Search"
