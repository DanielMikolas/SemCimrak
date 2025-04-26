
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

    def plot_sample_categories_pie(self):
        """
        Koláčový graf zobrazujúci rozdelenie vzoriek podľa kategórií (1, 2, 3).
        """
        counts = {1: 0, 2: 0, 3: 0}
        for sample in self.system.samples:
            counts[sample.category] += 1

        labels = ['Kategória 1', 'Kategória 2', 'Kategória 3']
        sizes = [counts[1], counts[2], counts[3]]
        colors = ['#66b3ff', '#99ff99', '#ffcc99']

        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('Rozdelenie vzoriek podľa kategórií')
        plt.axis('equal')  # kruh bude pekne okrúhly
        plt.show()

    def plot_average_waiting_samples(self):
        """
        Stĺpcový graf zobrazujúci priemerný počet čakajúcich vzoriek podľa kategórií počas simulovaného dňa.
        """
        averages = []
        categories = [1, 2, 3]
        for cat in categories:
            avg = sum(self.system.waiting_counts[cat]) / len(self.system.waiting_counts[cat])
            averages.append(avg)

        plt.figure(figsize=(8, 6))
        plt.bar(['Kategória 1', 'Kategória 2', 'Kategória 3'], averages, color=['#66b3ff', '#99ff99', '#ffcc99'])
        plt.xlabel('Kategória vzorky')
        plt.ylabel('Priemerný počet čakajúcich vzoriek')
        plt.title('Priemerný počet čakajúcich vzoriek podľa kategórií')
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    def plot_on_time_vs_late_samples(self):
        """
        Koláčový graf zobrazujúci podiel načas a neskoro dokončených vzoriek.
        """
        on_time = 0
        late = 0
        for sample in self.system.samples:
            if sample.completed_in_time:
                on_time += 1
            else:
                late += 1

        labels = ['Načas', 'Neskoro']
        sizes = [on_time, late]
        colors = ['#8bc34a', '#f44336']

        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('Podiel načas vs neskoro dokončených vzoriek')
        plt.axis('equal')  # Aby bol graf kruhový
        plt.tight_layout()
        plt.show()
