from src.domain.patient import MAX_HEALTH, MIN_HEALTH, Patient
from src.distributions.distributions import normal


def compute_deterioration(patient: Patient) -> float:
    noise = normal(mu=1.0, sigma=0.10204)
    deterioration = patient.deterioration_rate * noise
    return min(10.0, max(1.0, deterioration)) / 10.0


def compute_improvement(patient: Patient) -> float:
    noise = normal(mu=1.0, sigma=0.10204)
    improvement = patient.improvement_rate * noise
    return min(10.0, max(1.0, improvement)) / 20.0


def deteriorate_patient(patient: Patient) -> None:
    delta = compute_deterioration(patient)
    patient.health_level = max(MIN_HEALTH, patient.health_level - delta)
    patient.update_minimum_health()
    if patient.health_level <= MIN_HEALTH:
        patient.die()


def improve_patient(patient: Patient) -> None:
    delta = compute_improvement(patient)
    patient.health_level = min(MAX_HEALTH, patient.health_level + delta)
    patient.update_minimum_health()
    if patient.health_level >= MAX_HEALTH:
        patient.discharge()
