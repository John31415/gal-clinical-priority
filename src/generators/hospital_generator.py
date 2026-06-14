from src.domain.hospital import Hospital
from src.domain.patient import Patient
from src.domain.resource_requirement import ResourceRequirement
from collections import defaultdict
from src.distributions.distributions import gamma
import math


def generate_hospital(
    patients: list[Patient], mean: float = 1.0, variance: float = 0.0
) -> Hospital:
    required_resources = _get_resources(patients=patients)
    slack_vector = [
        _generate_slack(mean=mean, variance=variance)
        for _ in range(len(required_resources))
    ]
    available_resources = defaultdict(float)
    for i, r in enumerate(required_resources):
        available_resources[r.resource] = math.ceil(r.quantity * slack_vector[i])
    hospital_capacity = math.ceil(
        _generate_slack(mean=mean, variance=variance) * len(patients)
    )
    return Hospital(capacity=hospital_capacity, available_resources=available_resources)


def _get_resources(patients: list[Patient]) -> list[ResourceRequirement]:
    dict = defaultdict(float)
    for p in patients:
        for r in p.required_resources:
            dict[r.resource] += r.quantity
    return [ResourceRequirement(r, q) for (r, q) in dict.items()]


def _generate_slack(mean: float, variance: float) -> float:
    if variance == 0.0:
        return mean
    return gamma(mean**2 / variance, variance / mean)
