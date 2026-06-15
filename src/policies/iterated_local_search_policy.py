from src.domain.hospital import Hospital
from src.domain.patient import Patient
from src.policies.base_policy import PriorityPolicy
from src.policies.utils import patient_order_evaluation
import random


class ILSPolicy(PriorityPolicy):

    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations

    def order_patients(
        self,
        patients: list[Patient],
        hospital: Hospital,
        arrivals: list[Patient] = [],
    ) -> list[Patient]:
        for new_patient in arrivals:
            patients = self._add_optimize(
                patients=patients,
                new_patient=new_patient,
                hospital=hospital,
                max_iterations=self.max_iterations,
            )
        return patients

    def _greedy_insertion(
        self, patients: list[Patient], new_patient: Patient, hospital: Hospital
    ) -> list[Patient]:
        local_patients = patients + [new_patient]
        order = list(range(len(local_patients)))
        best_cost = patient_order_evaluation(
            permutation=order, patients=local_patients, hospital=hospital
        )
        best_order = list(order)
        for i in range(len(order) - 1, 0, -1):
            order[i], order[i - 1] = order[i - 1], order[i]
            cost = patient_order_evaluation(
                permutation=order, patients=local_patients, hospital=hospital
            )
            if cost > best_cost:
                best_cost = cost
                best_order = order.copy()
        return [local_patients[i] for i in best_order]

    def _hill_climbing(
        self, patients: list[Patient], hospital: Hospital
    ) -> list[Patient]:
        best_order = list(range(len(patients)))
        best_cost = patient_order_evaluation(
            permutation=best_order, patients=patients, hospital=hospital
        )
        improvement = True
        while improvement:
            improvement = False
            for i in range(len(best_order) - 1):
                order = best_order.copy()
                order[i], order[i + 1] = order[i + 1], order[i]
                cost = patient_order_evaluation(
                    permutation=order, patients=patients, hospital=hospital
                )
                if cost > best_cost:
                    best_cost = cost
                    best_order = order
                    improvement = True
                    break
        return [patients[i] for i in best_order]

    def _perturbation(self, patients: list[Patient]) -> list[Patient]:
        if len(patients) < 2:
            return patients
        p = list(patients)
        i = random.randint(0, len(p) - 1)
        j = random.randint(0, len(p) - 2)
        if j >= i:
            j += 1
        p[i], p[j] = p[j], p[i]
        return p

    def _add_optimize(
        self,
        patients: list[Patient],
        new_patient: Patient,
        hospital: Hospital,
        max_iterations: int,
    ) -> list[Patient]:
        patients = self._greedy_insertion(
            patients=patients, new_patient=new_patient, hospital=hospital
        )
        current_patients = self._hill_climbing(patients=patients, hospital=hospital)
        current_cost = patient_order_evaluation(
            permutation=list(range(len(current_patients))),
            patients=current_patients,
            hospital=hospital,
        )
        best_patients = list(current_patients)
        best_cost = current_cost
        for _ in range(max_iterations):
            shaken_patients = self._perturbation(current_patients)
            candidate_patients = self._hill_climbing(
                patients=shaken_patients, hospital=hospital
            )
            candidate_cost = patient_order_evaluation(
                permutation=list(range(len(candidate_patients))),
                patients=candidate_patients,
                hospital=hospital,
            )
            if candidate_cost >= current_cost:
                current_patients = candidate_patients
                current_cost = candidate_cost
            if candidate_cost > best_cost:
                best_patients = list(candidate_patients)
                best_cost = candidate_cost
        return best_patients

    def __repr__(self):
        return "Iterated Local Search Policy"
