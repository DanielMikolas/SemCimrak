import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Plotter:
    def __init__(self, system):
        self.system = system  # inštancia LabSystem, z ktorej budeme brať údaje

    def plot_waiting_samples(self):
        """
        Tento graf zobrazuje počet čakajúcich vzoriek v jednotlivých kategóriách (1, 2, 3) počas simulovaného dňa.
        """
        plt.figure(figsize=(12, 6))
        base_time = datetime.strptime("07:00", "%H:%M")
        times = [base_time + timedelta(minutes=i) for i in range(len(self.system.waiting_counts[1]))]
        time_labels = [t.strftime("%H:%M") for t in times]

        for cat in [1, 2, 3]:
            plt.plot(time_labels, self.system.waiting_counts[cat], label=f'Kategória {cat}')

        plt.xlabel("Čas")
        plt.ylabel("Počet čakajúcich vzoriek")
        plt.title("Počet čakajúcich vzoriek podľa kategórie počas dňa")
        plt.xticks(time_labels[::20], rotation=45)  # zobraz každých 20 minút
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
