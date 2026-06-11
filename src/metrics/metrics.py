from src.domain.patient import Patient, PatientStatus


def lives_saved(patients: list[Patient]) -> int:
    return sum(patient.status == PatientStatus.DISCHARGED for patient in patients)


def deaths(patients: list[Patient]) -> int:
    return sum(patient.status == PatientStatus.DECEASED for patient in patients)


def minimum_health_sum(patients: list[Patient]) -> float:
    return sum(patient.minimum_health_reached for patient in patients)


def evaluate_solution(patients: list[Patient]) -> tuple[int, float]:
    return (lives_saved(patients), minimum_health_sum(patients))


def simulation_statistics(patients: list[Patient]) -> dict:
    return {
        "patients": len(patients),
        "lives_saved": lives_saved(patients),
        "deaths": deaths(patients),
        "minimum_health_sum": minimum_health_sum(patients),
    }
