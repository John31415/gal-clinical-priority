from src.algorithms.simulated_annealing import State, simulated_annealing
from src.policies.base_policy import PriorityPolicy
from src.domain.hospital import Hospital
from src.domain.patient import Patient
from src.simulation.basic_simulator import BasicSimulator
from src.metrics.metrics import simulation_statistics
from src.policies.utils import patient_order_evaluation
from copy import deepcopy
import random


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

        def f_eval(permutation: list[int]) -> float:
            return patient_order_evaluation(
                permutation=permutation, patients=patients, hospital=hospital
            )

        state = PermState(random_order, f_eval)
        best_state = simulated_annealing(state)
        return [patients[i] for i in best_state.s]

    def __repr__(self):
        return "Simulated Annealing Policy"
