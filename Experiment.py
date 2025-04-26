from LabSystem import LabSystem


class Experiment:
    """
    Trieda pre simuláciu rôznych nastavení počtu technikov a výpočet priemerného oneskorenia.
    """

    def __init__(self, max_workers=50, simulations_per_setting=50):
        """
        Inicializácia experimentu.

        :param max_workers: Maximálny počet technikov, s ktorým sa experiment bude vykonávať.
        :param simulations_per_setting: Počet simulácií, ktoré sa vykonajú pre každý počet technikov.
        """
        self.max_workers = max_workers  # Maximálny počet technikov
        self.simulations_per_setting = simulations_per_setting  # Počet simulácií pre každý počet technikov
        self.results = []  # Ukladá výsledky experimentu

    def run(self):
        """
        Spustí experiment pre rôzne nastavenia počtu technikov.
        Pre každý počet technikov sa vykoná niekoľko simulácií a vypočíta sa priemerný pomer neskoro spracovaných vzoriek.
        """
        # Pre každý počet technikov od 1 do max_workers
        for num_workers in range(1, self.max_workers + 1):
            late_ratios = []  # Zoznam na ukladanie pomeru neskoro spracovaných vzoriek pre každú simuláciu

            # Simulácie pre každý počet technikov
            for _ in range(self.simulations_per_setting):
                system = LabSystem(num_workers)  # Vytvorenie systému s daným počtom technikov
                system.simulate_day()  # Simulácia jedného pracovného dňa
                late_ratio = system.get_late_ratio()  # Získanie pomeru neskoro spracovaných vzoriek
                late_ratios.append(late_ratio)  # Uloženie pomeru pre túto simuláciu
                print("Simulácia pre počet technikov:", num_workers)

            # Výpočet priemerného pomeru neskoro spracovaných vzoriek
            avg_late = sum(late_ratios) / len(late_ratios)
            self.results.append((num_workers, avg_late))  # Uloženie výsledkov pre tento počet technikov
            print(f"Technikov: {num_workers}, Priemerné % neskoro: {avg_late:.2%}")

            # Ak je priemerný pomer neskoro spracovaných vzoriek <= 3%, ukončíme experiment
            if avg_late <= 0.03:
                print(f"\n✅ Najmenší počet technikov s <= 3% oneskorením: {num_workers}")
                break

    def get_results(self):
        """
        Vráti výsledky experimentu (zoznam počtu technikov a priemerného pomeru neskoro spracovaných vzoriek).

        :return: Zoznam výsledkov experimentu
        """
        return self.results
