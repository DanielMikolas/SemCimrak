import random


class LabTechnician:
    def __init__(self, name, simulate_breaks=False):
        self.name = name
        self.busy_until = 0  # čas do kedy je zaneprázdnený
        self.samples_processed = []
        self.busy_time = 0
        self.simulate_breaks = simulate_breaks  # Určujeme, či sa simulujú prestávky
        self.work_time_since_break = 0  # koľko minút pracuje bez prestávky

    def is_available(self, current_time):
        return current_time >= self.busy_until

    def process_sample(self, sample, current_time, process_duration):
        sample.start_time = current_time
        sample.process_time = process_duration
        sample.completed_time = current_time + process_duration
        sample.completed_in_time = (sample.completed_time - sample.arrival_time <= sample.deadline_minutes)

        self.busy_until = sample.completed_time
        self.samples_processed.append(sample)
        self.busy_time += process_duration
        self.work_time_since_break += process_duration  # Pridávame čas do práce

        # Simulácia prestávok pre technika
        if self.simulate_breaks and self.work_time_since_break >= 90:  # Ak odpracoval viac ako 90 minút
            if random.random() < 0.5:  # 50% šanca, že si technik dá prestávku
                break_duration = random.randint(5, 10)  # Prestávka 5-10 minút
                self.busy_until += break_duration  # Posúvame čas, kedy bude technik opäť k dispozícii
                self.work_time_since_break = 0  # Resetujeme čas od poslednej prestávky

