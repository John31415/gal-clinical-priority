from dataclasses import dataclass


@dataclass
class BasicPatient:
    id: str
    age: int
    triage: str
    disease: str
    drugs: list[str]
