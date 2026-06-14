from src.domain.patient import Patient
from src.domain.hospital import Hospital
from src.simulation.basic_simulator import BasicSimulator
from src.metrics.metrics import simulation_statistics
from copy import deepcopy


def patient_order_evaluation(
    permutation: list[int], patients: list[Patient], hospital: Hospital
) -> float:
    ordered_patients = [patients[i] for i in permutation]
    simulator = BasicSimulator(
        hospital=deepcopy(hospital), patients=deepcopy(ordered_patients)
    )
    ordered_patients = simulator.run()
    stats = simulation_statistics(ordered_patients)
    return stats["lives_saved"] * 1000000 + stats["minimum_health_sum"]
