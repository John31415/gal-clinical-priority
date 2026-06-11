from dataclasses import dataclass, field
from src.domain.patient import Patient
from src.domain.resource import Resource


@dataclass
class Hospital:
    capacity: int
    available_resources: dict[Resource, float]
    admitted_patients: list[Patient] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be greater than zero")
        for quantity in self.available_resources.values():
            if quantity < 0:
                raise ValueError("resource quantities must be non-negative")

    @property
    def occupied_capacity(self) -> int:
        return len(self.admitted_patients)

    @property
    def free_capacity(self) -> int:
        return self.capacity - self.occupied_capacity

    def has_free_capacity(self) -> bool:
        return self.free_capacity > 0

    def has_required_resources(self, patient: Patient) -> bool:
        for requirement in patient.required_resources:
            available = self.available_resources.get(requirement.resource, 0)
            if available < requirement.quantity:
                return False
        return True

    def can_admit(self, patient: Patient) -> bool:
        return self.has_free_capacity() and self.has_required_resources(patient)

    def admit_patient(self, patient: Patient) -> bool:
        if not self.can_admit(patient):
            return False
        patient.admit()
        self.admitted_patients.append(patient)
        return True

    def release_patient(self, patient: Patient) -> None:
        self.admitted_patients.remove(patient)

    def __repr__(self) -> str:
        return (
            f"Hospital("
            f"capacity={self.capacity}, "
            f"occupied={self.occupied_capacity}, "
            f"resources={len(self.available_resources)}"
            f")"
        )
