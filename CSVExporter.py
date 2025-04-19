import csv
from LabTechnician import LabTechnician
from Sample import Sample

class CSVExporter:
    def __init__(self):
        pass

    def save_technicians_to_csv(self, technicians, filename="technicians_stats.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Meno", "Vyťaženosť (%)", "Počet vzoriek"])
            for tech in technicians:
                # Vyťaženosť technika je jeho čas spracovania vzoriek / celkový čas
                utilization = (min(tech.busy_time, 240) / 240) * 100  # predpokladáme, že simulácia trvá 240 minút
                writer.writerow([tech.name, f"{utilization:.2f}", len(tech.samples_processed)])

    def save_samples_to_csv(self, samples, filename="samples.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Príchod", "Kategória", "Deadline", "Začiatok", "Koniec", "Načas"])
            for sample in samples:
                writer.writerow([
                    sample.arrival_time,
                    sample.category,
                    sample.deadline_minutes,
                    sample.start_time,
                    sample.completed_time,
                    sample.completed_in_time
                ])
