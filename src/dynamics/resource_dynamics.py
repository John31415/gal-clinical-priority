from src.domain.patient import Patient


def health_factor(patient: Patient) -> float:
    return (11.0 - patient.health_level) / 10.0


def compute_resource_consumption(patient: Patient) -> float:
    return patient.improvement_rate * health_factor(patient)
