from dataclasses import dataclass, field
from enum import Enum
from src.domain.resource_requirement import ResourceRequirement

MIN_HEALTH = 1.0
MAX_HEALTH = 10.0


class PatientStatus(Enum):
    PENDING = "pending"
    WAITING = "waiting"
    ADMITTED = "admitted"
    DISCHARGED = "discharged"
    DECEASED = "deceased"


@dataclass
class Patient:
    id: str
    age: int
    diagnosis: str
    health_level: float
    deterioration_rate: float
    improvement_rate: float
    required_resources: list[ResourceRequirement]
    consumed_resources: dict
    status: PatientStatus = PatientStatus.PENDING
    time_waiting: int = 0
    time_admitted: int = 0
    minimum_health_reached: float = field(init=False)

    def __post_init__(self) -> None:
        self._validate()
        self.minimum_health_reached = self.health_level
        self.consumed_resources = {r.resource: 0 for r in self.required_resources}

    def _validate(self) -> None:
        if not (MIN_HEALTH <= self.health_level <= MAX_HEALTH):
            raise ValueError(f"health_level must be in [{MIN_HEALTH}, {MAX_HEALTH}]")

        if not (1 <= self.deterioration_rate <= 10):
            raise ValueError("deterioration_rate must be in [1, 10]")

        if not (1 <= self.improvement_rate <= 10):
            raise ValueError("improvement_rate must be in [1, 10]")

    @property
    def is_alive(self) -> bool:
        return self.status != PatientStatus.DECEASED

    @property
    def is_admitted(self) -> bool:
        return self.status == PatientStatus.ADMITTED

    @property
    def is_waiting(self) -> bool:
        return self.status == PatientStatus.WAITING

    @property
    def is_pending(self) -> bool:
        return self.status == PatientStatus.PENDING

    @property
    def is_finished(self) -> bool:
        return self.status in {
            PatientStatus.DISCHARGED,
            PatientStatus.DECEASED,
        }

    def update_minimum_health(self) -> None:
        self.minimum_health_reached = min(
            self.minimum_health_reached,
            self.health_level,
        )

    def admit(self) -> None:
        self.status = PatientStatus.ADMITTED

    def discharge(self) -> None:
        self.status = PatientStatus.DISCHARGED

    def wait(self) -> None:
        self.status = PatientStatus.WAITING

    def die(self) -> None:
        self.status = PatientStatus.DECEASED

    def __repr__(self) -> str:
        return (
            f"Patient("
            f"id={self.id}, "
            f"health={self.health_level:.2f}, "
            f"status={self.status.value}"
            f")"
        )
