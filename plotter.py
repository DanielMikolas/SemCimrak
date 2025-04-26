import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class Plotter:
    def __init__(self, system):
        """
        Inštanciácia triedy Plotter, ktorá bude pracovať s inštanciou LabSystem na zobrazenie grafov.

        :param system: Objekt LabSystem, z ktorého budeme čerpať dáta.
        """
        self.system = system  # inštancia LabSystem, z ktorej budeme brať údaje

    def plot_waiting_samples(self):
        """
        Vykreslí graf zobrazujúci počet čakajúcich vzoriek v jednotlivých kategóriách (1, 2, 3)
        počas simulovaného dňa.
        """
        # Nastavenie grafu
        plt.figure(figsize=(12, 6))

        # Základný čas (7:00 AM)
        base_time = datetime.strptime("07:00", "%H:%M")

        # Generovanie času pre x-ovú os (časový rámec od 7:00 do 11:00)
        times = [base_time + timedelta(minutes=i) for i in range(len(self.system.waiting_counts[1]))]
        time_labels = [t.strftime("%H:%M") for t in times]

        # Vykreslenie grafu pre každú kategóriu (1, 2, 3)
        for cat in [1, 2, 3]:
            plt.plot(time_labels, self.system.waiting_counts[cat], label=f'Kategória {cat}')

        # Popisy osí a názov grafu
        plt.xlabel("Čas")
        plt.ylabel("Počet čakajúcich vzoriek")
        plt.title("Počet čakajúcich vzoriek podľa kategórie počas dňa")

        # Úprava zobrazenia osí
        plt.xticks(time_labels[::20], rotation=45)  # zobraz každých 20 minút

        # Zobrazenie legendy a mriežky
        plt.legend()
        plt.grid(True)

        # Vytvorenie grafu
        plt.tight_layout()
        plt.show()

    def plot_sample_categories_pie(self):
        """
        Vykreslí koláčový graf zobrazujúci rozdelenie vzoriek podľa kategórií (1, 2, 3).
        """
        # Počítanie vzoriek podľa kategórií
        counts = {1: 0, 2: 0, 3: 0}
        for sample in self.system.samples:
            counts[sample.category] += 1

        # Nastavenie popisov a veľkostí koláčového grafu
        labels = ['Kategória 1', 'Kategória 2', 'Kategória 3']
        sizes = [counts[1], counts[2], counts[3]]
        colors = ['#66b3ff', '#99ff99', '#ffcc99']  # Určenie farieb pre jednotlivé kategórie

        # Vykreslenie koláčového grafu
        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('Rozdelenie vzoriek podľa kategórií')
        plt.axis('equal')  # Zabezpečenie, že graf bude kruhový

        # Zobrazenie grafu
        plt.show()

    def plot_average_waiting_samples(self):
        """
        Vykreslí stĺpcový graf zobrazujúci priemerný počet čakajúcich vzoriek podľa kategórií
        počas simulovaného dňa.
        """
        # Výpočet priemerného počtu čakajúcich vzoriek pre každú kategóriu
        averages = []
        categories = [1, 2, 3]
        for cat in categories:
            avg = sum(self.system.waiting_counts[cat]) / len(self.system.waiting_counts[cat])
            averages.append(avg)

        # Vykreslenie stĺpcového grafu
        plt.figure(figsize=(8, 6))
        plt.bar(['Kategória 1', 'Kategória 2', 'Kategória 3'], averages, color=['#66b3ff', '#99ff99', '#ffcc99'])
        plt.xlabel('Kategória vzorky')
        plt.ylabel('Priemerný počet čakajúcich vzoriek')
        plt.title('Priemerný počet čakajúcich vzoriek podľa kategórií')

        # Úprava zobrazenia mriežky
        plt.grid(axis='y')

        # Zobrazenie grafu
        plt.tight_layout()
        plt.show()

    def plot_on_time_vs_late_samples(self):
        """
        Vykreslí koláčový graf zobrazujúci podiel načas a neskoro dokončených vzoriek.
        """
        # Počítanie vzoriek, ktoré boli dokončené načas a neskoro
        on_time = 0
        late = 0
        for sample in self.system.samples:
            if sample.completed_in_time:
                on_time += 1
            else:
                late += 1

        # Nastavenie popisov a veľkostí koláčového grafu
        labels = ['Načas', 'Neskoro']
        sizes = [on_time, late]
        colors = ['#8bc34a', '#f44336']  # Farby pre "načas" a "neskoro"

        # Vykreslenie koláčového grafu
        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('Podiel načas vs neskoro dokončených vzoriek')
        plt.axis('equal')  # Zabezpečenie, že graf bude kruhový

        # Zobrazenie grafu
        plt.tight_layout()
        plt.show()
