import random
from collections import deque

from CSVExporter import CSVExporter
from LabTechnician import LabTechnician
from Sample import Sample
from plotter import Plotter  # importujeme Plotter

class LabSystem:
    """
    Trieda pre simuláciu systému laboratória, ktorý spracováva vzorky.
    """

    def __init__(self, num_technicians, simulate_breaks=False):
        """
        Inicializácia laboratórneho systému.

        :param num_technicians: Počet technikov, ktorí budú pracovať v laboratóriu.
        :param simulate_breaks: Určuje, či budú technici simulovať prestávky počas dňa.
        """
        self.time = 0  # Čas v minútach od 7:00
        self.samples = []  # Zoznam všetkých vzoriek
        self.technicians = [LabTechnician(f"Tech_{i + 1}", simulate_breaks) for i in range(num_technicians)]  # Technici
        self.queues = {1: deque(), 2: deque(), 3: deque()}  # Riadky pre jednotlivé kategórie vzoriek
        self.waiting_counts = {1: [], 2: [], 3: []}  # Počty čakajúcich vzoriek pre grafy
        self.stats = {'late': 0, 'total': 0}  # Štatistiky počtu vzoriek

        self.plotter = Plotter(self)  # Inštancia triedy pre tvorbu grafov

        self.exporter = CSVExporter()  # Inštancia na export dát do CSV

    def generate_samples(self):
        """
        Generovanie vzoriek na základe náhodných parametrov pre 28 ambulancií.
        Každá ambulancia bude mať náhodný počet vzoriek.
        """
        for _ in range(28):  # 28 ambulancií
            count = random.randint(40, 60)  # Počet vzoriek pre jednu ambulanciu
            for _ in range(count):
                arrival = random.randint(0, 120)  # Čas príchodu vzorky medzi 7:00 a 9:00
                rnd = random.random()
                if rnd < 1 / 6:
                    category, deadline = 1, 20  # Kategória 1 (deadline do 20 minút)
                elif rnd < 0.5:
                    category, deadline = 2, 60  # Kategória 2 (deadline do 60 minút)
                else:
                    category, deadline = 3, 180  # Kategória 3 (deadline do 180 minút)
                self.samples.append(Sample(arrival, category, deadline))
        self.samples.sort(key=lambda s: s.arrival_time)  # Zoradenie vzoriek podľa času príchodu

    def simulate_day(self):
        """
        Simulácia jedného pracovného dňa od 7:00 do 11:00.
        Technici spracovávajú vzorky v poradí príchodu a podľa kategórií.
        """
        sample_idx = 0  # Index aktuálnej vzorky
        for self.time in range(0, 240):  # Pracovný čas od 7:00 do 11:00
            # Doručenie nových vzoriek
            while sample_idx < len(self.samples) and self.samples[sample_idx].arrival_time == self.time:
                s = self.samples[sample_idx]
                self.queues[s.category].append(s)  # Pridanie vzorky do príslušného radu
                sample_idx += 1

            # Technici spracovávajú vzorky podľa dostupnosti
            for tech in self.technicians:
                if tech.is_available(self.time):
                    sample = self.get_next_sample()  # Získať ďalšiu vzorku z radu
                    if sample:
                        # Generovanie doby spracovania vzorky pomocou trojuholníkového rozdelenia
                        duration = round(random.triangular(5, 9, 7))  # Doba spracovania (zaokrúhlená na celé minúty)
                        tech.process_sample(sample, self.time, duration)  # Spracovanie vzorky technikom

            # Zaznamenávanie počtu čakajúcich vzoriek pre grafy
            for cat in [1, 2, 3]:
                self.waiting_counts[cat].append(len(self.queues[cat]))

    def get_next_sample(self):
        """
        Získa ďalšiu vzorku z radu podľa priority kategórie (od kategórie 1 po 3).
        """
        for cat in [1, 2, 3]:
            if self.queues[cat]:
                return self.queues[cat].popleft()  # Vráti vzorku z prvej kategórie, ktorá nie je prázdna
        return None  # Ak nie sú žiadne vzorky na spracovanie

    def collect_stats(self):
        """
        Získa štatistiky počtu vzoriek, ktoré boli spracované načas a celkového počtu vzoriek.
        """
        total = [0, 0, 0]  # Počty vzoriek v jednotlivých kategóriách
        on_time = [0, 0, 0]  # Počty vzoriek spracovaných načas v jednotlivých kategóriách
        for s in self.samples:
            cat = s.category - 1
            total[cat] += 1
            if s.completed_in_time:
                on_time[cat] += 1

        # Aktualizácia štatistík
        self.stats['total'] = sum(total)
        self.stats['late'] = sum(total) - sum(on_time)

        return total, on_time  # Vrátenie počtu vzoriek a počtu načas spracovaných vzoriek

    def get_late_ratio(self):
        """
        Získa pomer neskoro spracovaných vzoriek.
        """
        if self.stats['total'] == 0:  # Ošetrenie delenia nulou
            return 0
        return self.stats['late'] / self.stats['total']

    def get_utilization(self):
        """
        Vypočíta vyťaženosť technikov (čas spracovania vzoriek / celkový pracovný čas).
        """
        utilization = []
        for tech in self.technicians:
            # Vyťaženosť technika (maximálny čas spracovania do 240 minút)
            util = min(tech.busy_time, 240) / 240
            utilization.append(util)
        return utilization  # Vrátenie zoznamu vyťaženosti technikov

    def save_data_to_csv(self):
        """
        Uloží dáta o technikoch a vzorkách do CSV súborov.
        """
        self.exporter.save_technicians_to_csv(self.technicians)  # Uloží technikov
        self.exporter.save_samples_to_csv(self.samples)  # Uloží vzorky
