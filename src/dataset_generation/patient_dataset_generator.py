from src.dataset_generation.patient_generator import json_patient_generator
from src.dataset_generation.dataset_utils import text2json, text_json_to_dict
from src.dataset_generation.basic_patient_generator import generate_basic_patient
from src.dataset_generation.diagnosis_generator import diagnosis_generator


def dataset_patient_generator(
    path: str = "dataset/patient_evaluation.json", total_patients: int = 300
) -> None:
    for _ in range(total_patients):
        basic_patient = generate_basic_patient()
        diagnosis = diagnosis_generator(basic_patient=basic_patient)
        patient_json_text = json_patient_generator(diagnosis=diagnosis)
        patient = {
            "id": basic_patient.id,
            "age": basic_patient.age,
            "diagnosis": diagnosis,
        }
        patient |= text_json_to_dict(patient_json_text)
        text2json(dict=patient, path=path)


# dataset_patient_generator()
