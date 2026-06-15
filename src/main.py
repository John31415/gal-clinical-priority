from src.generators.scenario_generator import generate_scenario
from src.simulation.intelligent_simulator import IntelligentSimulator
from src.metrics.metrics import simulation_statistics
from src.policies.base_policy import PriorityPolicy
from src.policies.simulated_annealing_policy import SimAnnealPolicy
from src.policies.random_policy import RandomPolicy
from src.policies.severity_policy import SeverityPolicy
from src.policies.negligent_policy import NegligentPolicy
from src.policies.iterated_local_search_policy import ILSPolicy
from src.domain.hospital import Hospital
from src.domain.patient import Patient
from src.policies.sa_ils_policy import SAILSPolicy
from copy import deepcopy
import time


def simulate_policy(
    hospital: Hospital, patients: list[Patient], policy: PriorityPolicy
) -> int:
    t = time.time()
    simulator = IntelligentSimulator(
        hospital=deepcopy(hospital),
        patients=deepcopy(patients),
        policy=deepcopy(policy),
    )
    patients = simulator.run()
    stats = simulation_statistics(patients)
    print(f"\n=== Simulation Results ({policy}) ===\n")
    print(f"Time elapsed: {simulator.time}\n")
    for key, value in stats.items():
        print(f"{key}: {value}")
    execution_time = time.time() - t
    print(f"Execution completed in {execution_time:.2f} seconds")
    return stats["lives_saved"]


def main() -> None:
    hospital, patients = generate_scenario(
        patient_count=180, shuffle_patients=True, mean=0.9, variance=0.3
    )
    policies = [
        RandomPolicy(),
        SeverityPolicy(),
        NegligentPolicy(),
        SimAnnealPolicy(),
        ILSPolicy(),
        SAILSPolicy(),
    ]
    best_policy = None
    max_lives_saved = 0
    for policy in policies:
        lives_saved = simulate_policy(
            hospital=deepcopy(hospital), patients=deepcopy(patients), policy=policy
        )
        if lives_saved >= max_lives_saved:
            max_lives_saved = lives_saved
            best_policy = policy
    print(f"\n=== Winner: {best_policy} ===\n")


if __name__ == "__main__":
    main()
