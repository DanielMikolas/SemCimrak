import csv
from LabTechnician import LabTechnician
from Sample import Sample


class CSVExporter:
    """
    Trieda zodpovedná za export dát o technikoch a vzorkách do CSV súborov.
    """

    def __init__(self):
        """
        Inicializácia triedy, ktorá nevyžaduje žiadne parametre.
        """
        pass

    def save_technicians_to_csv(self, technicians, filename="technicians_stats.csv"):
        """
        Uloží štatistiky o technikoch (vyťaženosť a počet spracovaných vzoriek) do CSV súboru.

        :param technicians: Zoznam technikov, ktorých štatistiky sa ukladajú.
        :param filename: Názov súboru, do ktorého sa štatistiky uložia (predvolený je "technicians_stats.csv").
        """
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Zapíše hlavičku do CSV súboru
            writer.writerow(["Meno", "Vyťaženosť (%)", "Počet vzoriek"])
            for tech in technicians:
                # Vyťaženosť technika: čas spracovania / celkový čas pracovného dňa (240 minút)
                utilization = (min(tech.busy_time, 240) / 240) * 100  # predpokladáme, že simulácia trvá 240 minút
                # Zapisuje údaje o technikovi (meno, vyťaženosť a počet spracovaných vzoriek)
                writer.writerow([tech.name, f"{utilization:.2f}", len(tech.samples_processed)])

    def save_samples_to_csv(self, samples, filename="samples.csv"):
        """
        Uloží údaje o vzorkách (príchod, kategória, deadline, začiatok spracovania, koniec spracovania, načas) do CSV súboru.

        :param samples: Zoznam vzoriek, ktorých údaje sa ukladajú.
        :param filename: Názov súboru, do ktorého sa údaje o vzorkách uložia (predvolený je "samples.csv").
        """
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Zapíše hlavičku do CSV súboru
            writer.writerow(["Príchod", "Kategória", "Deadline", "Začiatok", "Koniec", "Načas"])
            for sample in samples:
                # Zapisuje údaje o každej vzorke (príchod, kategória, deadline, začiatok a koniec spracovania)
                writer.writerow([
                    sample.arrival_time,
                    sample.category,
                    sample.deadline_minutes,
                    sample.start_time,
                    sample.completed_time,
                    sample.completed_in_time
                ])
