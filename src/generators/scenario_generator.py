from src.generators.hospital_generator import generate_hospital
from src.utils.load_json import load_json
from src.domain.patient import Patient
from src.domain.resource_requirement import ResourceRequirement
import random


def get_patients(patient_count: int, shuffle: bool) -> list[Patient]:
    patients_json = load_json()
    patients = [
        Patient(
            id=p["id"],
            age=p["age"],
            diagnosis=p["diagnosis"],
            health_level=p["health_level"],
            deterioration_rate=p["deterioration_rate"],
            improvement_rate=p["improvement_rate"],
            required_resources=[ResourceRequirement(d[0], d[1]) for d in p["drugs"]],
        )
        for p in patients_json
    ]
    if shuffle:
        random.shuffle(patients)
    return patients[:patient_count]


def generate_scenario(patient_count: int, shuffle_patients: bool = False):
    patients = get_patients(patient_count, shuffle_patients)
    hospital = generate_hospital(patients=patients, mean=0.75, variance=0.5)
    return hospital, patients
