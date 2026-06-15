from src.generators.scenario_generator import generate_scenario
from src.simulation.intelligent_simulator import IntelligentSimulator
from src.metrics.metrics import simulation_statistics
from src.policies.base_policy import PriorityPolicy
from src.domain.hospital import Hospital
from src.domain.patient import Patient
from src.experiments.experiments import generate_experiment
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
    print(f"Parameters:\n{policy.sig()}\n")
    print(f"Time elapsed: {simulator.time}\n")
    for key, value in stats.items():
        print(f"{key}: {value}")
    execution_time = time.time() - t
    print(f"Execution completed in {execution_time:.2f} seconds")
    return stats["lives_saved"]


def main() -> None:
    hospital, patients, policies = generate_experiment()
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
