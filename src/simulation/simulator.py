from src.domain.hospital import Hospital
from src.domain.patient import Patient, PatientStatus
from src.dynamics.health_dynamics import deteriorate_patient, improve_patient
from src.policies.base_policy import PriorityPolicy


class Simulator:

    def __init__(
        self, hospital: Hospital, patients: list[Patient], policy: PriorityPolicy
    ) -> None:
        self.hospital = hospital
        self.patients = patients
        self.policy = policy
        self.time = 0

    def run(self) -> None:
        while not self.is_finished():
            self.step()

    def step(self) -> None:
        self._admit_patients()
        self._update_admitted_patients()
        self._update_waiting_patients()
        self.time += 1

    def is_finished(self) -> bool:
        return all(patient.is_finished for patient in self.patients)

    def _admit_patients(self) -> None:
        for patient in self.patients:
            if not self.hospital.has_free_capacity():
                break
            if not patient.is_waiting:
                continue
            if self.hospital.can_admit(patient):
                self.hospital.admit_patient(patient)
            else:
                break

    def _update_admitted_patients(self) -> None:
        discharged = []
        deceased = []
        for patient in self.hospital.admitted_patients:
            improve_patient(patient)
            patient.time_admitted += 1
            if patient.status == PatientStatus.DISCHARGED:
                discharged.append(patient)
            elif patient.status == PatientStatus.DECEASED:
                deceased.append(patient)
        for patient in discharged:
            self.hospital.release_patient(patient)
        for patient in deceased:
            self.hospital.release_patient(patient)

    def _update_waiting_patients(self) -> None:
        for patient in self.patients:
            if not patient.is_waiting:
                continue
            deteriorate_patient(patient)
            patient.time_waiting += 1
