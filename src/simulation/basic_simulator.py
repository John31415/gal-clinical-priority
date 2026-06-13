from src.simulation.base_simulator import BaseSimulator


class BasicSimulator(BaseSimulator):

    def step(self) -> None:
        if self.is_finished():
            return
        self._admit_from_queue()
        self._advance_admitted_patients()
        self._advance_waiting_patients()
        self.time += 1

    def _initialize(self) -> None:
        self.waiting_queue = []
        for patient in self.patients:
            if patient.is_finished:
                continue
            patient.wait()
            self.waiting_queue.append(patient)
