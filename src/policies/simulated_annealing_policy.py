from src.algorithms.simulated_annealing import State, simulated_annealing
from src.policies.base_policy import PriorityPolicy
from src.domain.hospital import Hospital
from src.domain.patient import Patient
from src.simulation.basic_simulator import BasicSimulator
from src.metrics.metrics import simulation_statistics
import random
from copy import deepcopy


class PermState(State):
    def __init__(self, s: list[int], f_eval):
        self.s = s
        self.f_eval = f_eval

    def next(self) -> State:
        len_s = len(self.s)
        if len_s <= 1:
            return PermState(s=self.s, f_eval=self.f_eval)
        i = random.randint(0, len_s - 1)
        j = random.randint(0, len_s - 2)
        if j >= i:
            j += 1
        s_next = deepcopy(self.s)
        s_next[i], s_next[j] = s_next[j], s_next[i]
        return PermState(s_next, self.f_eval)

    def E(self):
        return -self.f_eval(self.s)


class SimAnnealPolicy(PriorityPolicy):

    def order_patients(
        self, patients: list[Patient], hospital: Hospital, arrivals: list[Patient] = []
    ) -> list[Patient]:
        patients += arrivals
        random_order = list(range(len(patients)))
        random.shuffle(random_order)

        def f_eval(p: list[int]) -> float:
            ordered_patients = [patients[i] for i in p]
            simulator = BasicSimulator(
                hospital=deepcopy(hospital), patients=deepcopy(ordered_patients)
            )
            ordered_patients = simulator.run()
            stats = simulation_statistics(ordered_patients)
            return stats["lives_saved"] * 1000000 + stats["minimum_health_sum"]

        state = PermState(random_order, f_eval)
        best_state = simulated_annealing(state)
        return [patients[i] for i in best_state.s]
