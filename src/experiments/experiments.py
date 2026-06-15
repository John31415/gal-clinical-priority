from src.policies.base_policy import PriorityPolicy
from src.domain.hospital import Hospital
from src.domain.patient import Patient
from src.generators.scenario_generator import generate_scenario
from src.distributions.distributions import uniform
from src.policies.simulated_annealing_policy import SimAnnealPolicy
from src.policies.random_policy import RandomPolicy
from src.policies.severity_policy import SeverityPolicy
from src.policies.negligent_policy import NegligentPolicy
from src.policies.iterated_local_search_policy import ILSPolicy
from src.policies.sa_ils_policy import SAILSPolicy
import math


def generate_experiment() -> tuple[Hospital, list[Patient], list[PriorityPolicy]]:
    patient_count = 180#math.ceil(uniform(20, 150))
    mean = 1.2#uniform(0.7, 1.2)
    variance = 0.7#uniform(0.02, 0.3)
    hospital, patients = generate_scenario(
        patient_count=patient_count,
        shuffle_patients=True,
        mean=mean,
        variance=variance,
    )
    t0 = 100#uniform(100, 500)
    decay = 0.7#uniform(0.8, 0.995)
    t_min = 1.0
    max_iterations = 2#math.ceil(uniform(10, 100))
    policies = [
        RandomPolicy(),
        SeverityPolicy(),
        NegligentPolicy(),
        SimAnnealPolicy(t0=t0, decay=decay, t_min=t_min),
        ILSPolicy(max_iterations=max_iterations),
        SAILSPolicy(t0=t0, decay=decay, t_min=t_min, max_iterations=max_iterations),
    ]
    return (hospital, patients, policies)
