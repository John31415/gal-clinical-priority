from src.domain.hospital import Hospital
from src.domain.patient import Patient, PatientStatus
from src.policies.base_policy import PriorityPolicy
from src.distributions.distributions import exponential
from src.simulation.base_simulator import BaseSimulator


class IntelligentSimulator(BaseSimulator):

    def __init__(
        self,
        hospital: Hospital,
        patients: list[Patient],
        policy: PriorityPolicy,
    ) -> None:
        self.hospital = hospital
        self.patients = list(patients)
        self.policy = policy
        self.time = 0
        self._mean_interarrival_time = 2.0
        self.waiting_queue: list[Patient] = []
        self._scheduled_arrivals: list[tuple[int, Patient]] = []
        self._arrival_cursor = 0
        self._initialize()

    def step(self) -> None:
        if self.is_finished():
            return
        arrivals = self._inject_arrivals()
        if arrivals:
            self.waiting_queue = self.policy.order_patients(
                patients=self.waiting_queue,
                hospital=self.hospital,
                arrivals=arrivals,
            )
        self._admit_from_queue()
        self._advance_admitted_patients()
        self._advance_waiting_patients()
        self.time += 1

    def _initialize(self) -> None:
        self.waiting_queue = []
        self._scheduled_arrivals = []
        current_time = 0
        for patient in self.patients:
            if patient.is_finished:
                continue
            current_time += max(
                0, int(round(exponential(self._mean_interarrival_time)))
            )
            self._scheduled_arrivals.append((current_time, patient))

    def _inject_arrivals(self) -> list[Patient]:
        arrivals = []
        while (
            self._arrival_cursor < len(self._scheduled_arrivals)
            and self._scheduled_arrivals[self._arrival_cursor][0] <= self.time
        ):
            _, patient = self._scheduled_arrivals[self._arrival_cursor]
            self._arrival_cursor += 1
            if patient.is_finished:
                continue
            patient.status = PatientStatus.WAITING
            arrivals.append(patient)
        return arrivals
