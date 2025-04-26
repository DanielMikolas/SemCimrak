import random
from collections import deque

from CSVExporter import CSVExporter
from LabTechnician import LabTechnician
from Sample import Sample
from plotter import Plotter  # importujeme Plotter

class LabSystem:
    def __init__(self, num_technicians, simulate_breaks=False):
        self.time = 0  # v minútach od 7:00
        self.samples = []
        # Pridanie parametra simulate_breaks do vytvárania technikov
        self.technicians = [LabTechnician(f"Tech_{i + 1}", simulate_breaks) for i in range(num_technicians)]
        self.queues = {1: deque(), 2: deque(), 3: deque()}
        self.waiting_counts = {1: [], 2: [], 3: []}  # pre grafy
        self.stats = {'late': 0, 'total': 0}  # inicializácia štatistík

        self.plotter = Plotter(self)  # vytvorenie inštancie Plotter, ale nebude sa volať priamo v simulácii

        self.exporter = CSVExporter()


    def generate_samples(self):
        for _ in range(28):  # ambulancie
            count = random.randint(40, 60)
            for _ in range(count):
                arrival = random.randint(0, 120)  # medzi 7:00 a 9:00
                rnd = random.random()
                if rnd < 1 / 6:
                    category, deadline = 1, 20
                elif rnd < 0.5:
                    category, deadline = 2, 60
                else:
                    category, deadline = 3, 180
                self.samples.append(Sample(arrival, category, deadline))
        self.samples.sort(key=lambda s: s.arrival_time)  # podľa času príchodu

    def simulate_day(self):
        sample_idx = 0
        for self.time in range(0, 240):  # od 7:00 do 11:00
            # doručenie nových vzoriek
            while sample_idx < len(self.samples) and self.samples[sample_idx].arrival_time == self.time:
                s = self.samples[sample_idx]
                self.queues[s.category].append(s)
                sample_idx += 1

            # každý pracovník dostane čo najskôr vzorku podľa priority
            for tech in self.technicians:
                if tech.is_available(self.time):
                    sample = self.get_next_sample()
                    if sample:
                        # toto je jedna moznost generovania dlzky trvania spracovania vzorky
                        #duration = random.choices([5, 6, 7, 8, 9], weights=[1, 2, 4, 2, 1])[0]

                        # toto je pouzitie trojuholnikoveho rozdelenia
                        duration = round(random.triangular(5, 9, 7))  # Výstup zaokrúhleny na celé minúty
                        tech.process_sample(sample, self.time, duration)

            # pre graf: zaznam počtu čakajúcich
            for cat in [1, 2, 3]:
                self.waiting_counts[cat].append(len(self.queues[cat]))

    def get_next_sample(self):
        for cat in [1, 2, 3]:
            if self.queues[cat]:
                return self.queues[cat].popleft()
        return None

    def collect_stats(self):
        total = [0, 0, 0]
        on_time = [0, 0, 0]
        for s in self.samples:
            cat = s.category - 1
            total[cat] += 1
            if s.completed_in_time:
                on_time[cat] += 1

        # Aktualizujeme štatistiky
        self.stats['total'] = sum(total)
        self.stats['late'] = sum(total) - sum(on_time)

        return total, on_time

    def get_late_ratio(self):
        if self.stats['total'] == 0:  # zabezpečenie delenia nulou
            return 0
        return self.stats['late'] / self.stats['total']

    def get_utilization(self):
        utilization = []
        for tech in self.technicians:
            util = min(tech.busy_time, 240) / 240 # 240 minút pracovného času
            utilization.append(util)
        return utilization

    def save_data_to_csv(self):
        # Uložíme dáta o technikoch a vzorkách do CSV
        self.exporter.save_technicians_to_csv(self.technicians)
        self.exporter.save_samples_to_csv(self.samples)