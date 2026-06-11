import uuid
import random
import math
from src.domain.basic_patient import BasicPatient
from src.distributions.distributions import beta
from src.dataset_generation.dataset_utils import get_top_diseases, disease2drug

diseases = get_top_diseases()


def generate_basic_patient() -> BasicPatient:
    id = uuid.uuid4().hex
    age = math.ceil(beta(1.62, 1.34, 0, 100))
    triage = random.choice(["Red", "Yellow", "Green"])
    disease = random.choice(diseases)
    drugs = disease2drug(disease=disease)
    basic_patient = BasicPatient(
        id=id,
        age=age,
        triage=triage,
        disease=disease,
        drugs=drugs,
    )
    return basic_patient
