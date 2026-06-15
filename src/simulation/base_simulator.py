from src.domain.hospital import Hospital
from src.domain.patient import Patient, PatientStatus
from src.domain.resource import Resource
from src.dynamics.health_dynamics import deteriorate_patient, improve_patient
from abc import ABC, abstractmethod


class BaseSimulator(ABC):

    def __init__(
        self,
        hospital: Hospital,
        patients: list[Patient],
    ) -> None:
        self.hospital = hospital
        self.patients = list(patients)
        self.time = 0
        self.waiting_queue: list[Patient] = []
        self._initialize()

    def run(self) -> list[Patient]:
        while not self.is_finished():
            self.step()
        return self.patients

    @abstractmethod
    def step(self):
        pass

    def is_finished(self) -> bool:
        return all(patient.is_finished for patient in self.patients)

    @abstractmethod
    def _initialize(self):
        pass

    def _admit_from_queue(self) -> None:
        while self.waiting_queue:
            first_patient = self.waiting_queue[0]
            if not self.hospital.can_admit(patient=first_patient):
                break
            self.hospital.admit_patient(patient=first_patient)
            self.waiting_queue.pop(0)

    def _advance_admitted_patients(self) -> None:
        for patient in list(self.hospital.admitted_patients):
            if self._consume_resources_for_patient(patient):
                improve_patient(patient)
            else:
                deteriorate_patient(patient)
            patient.time_admitted += 1
            if (
                patient.status == PatientStatus.DISCHARGED
                or patient.status == PatientStatus.DECEASED
            ):
                self.hospital.release_patient(patient)

    def _advance_waiting_patients(self) -> None:
        new_queue: list[Patient] = []
        for patient in self.waiting_queue:
            deteriorate_patient(patient)
            patient.time_waiting += 1
            if patient.status != PatientStatus.DECEASED:
                new_queue.append(patient)
        self.waiting_queue = new_queue

    def _consume_resources_for_patient(self, patient: Patient) -> bool:
        if not patient.required_resources:
            return True
        required_amounts: list[tuple[Resource, float]] = []
        for r in patient.required_resources:
            amount = max(
                0.0,
                r.quantity - patient.consumed_resources[r.resource],
            )
            required_amounts.append((r.resource, amount))
        for resource, amount in required_amounts:
            if self.hospital.available_resources.get(resource, 0.0) < amount:
                return False
        for resource, amount in required_amounts:
            self.hospital.available_resources[resource] -= amount
            patient.consumed_resources[resource] += amount
        return True
