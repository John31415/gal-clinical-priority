from src.policies.base_policy import PriorityPolicy
from src.policies.simulated_annealing_policy import SimAnnealPolicy
from src.policies.iterated_local_search_policy import ILSPolicy
from src.domain.hospital import Hospital
from src.domain.patient import Patient


class SAILSPolicy(PriorityPolicy):

    def __init__(
        self,
        t0: float = 100.0,
        decay: float = 0.9,
        t_min: float = 1.0,
        max_iterations: int = 1,
    ):
        self.t0 = t0
        self.decay = decay
        self.t_min = t_min
        self.max_iterations = max_iterations

    def order_patients(
        self, patients: list[Patient], hospital: Hospital, arrivals: list[Patient] = []
    ) -> list[Patient]:
        return SimAnnealPolicy(
            t0=self.t0, decay=self.decay, t_min=self.t_min
        ).order_patients(
            patients=ILSPolicy(max_iterations=self.max_iterations).order_patients(
                patients=patients, hospital=hospital, arrivals=arrivals
            ),
            hospital=hospital,
        )

    def __repr__(self):
        return "Hybrid Policy: Simulated Annealing and Iterated Local Search"
