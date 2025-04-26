# experiment.py
from LabSystem import LabSystem

class Experiment:
    def __init__(self, max_workers=50, simulations_per_setting= 50 ):
        self.max_workers = max_workers
        self.simulations_per_setting = simulations_per_setting
        self.results = []

    def run(self):
        for num_workers in range(1, self.max_workers + 1):
            late_ratios = []

            for _ in range(self.simulations_per_setting):
                system = LabSystem(num_workers)
                system.simulate_day()
                late_ratio = system.get_late_ratio()
                late_ratios.append(late_ratio)
                print("simulation")

            avg_late = sum(late_ratios) / len(late_ratios)
            self.results.append((num_workers, avg_late))
            print(f"Technikov: {num_workers}, Priemerné % neskoro: {avg_late:.2%}")

            if avg_late <= 0.03:
                print(f"\n✅ Najmenší počet technikov s <= 3% oneskorením: {num_workers}")
                break

    def get_results(self):
        return self.results