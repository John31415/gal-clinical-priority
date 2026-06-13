from src.domain.patient import Patient, MAX_HEALTH


def compute_resource_consumption(patient: Patient) -> float:
    x = (patient.health_level - patient.minimum_health_reached) / (
        MAX_HEALTH - patient.minimum_health_reached
    )
    return 2 * x - x**2
