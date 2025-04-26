from LabSystem import LabSystem
from Experiment import Experiment
from LabTechnician import LabTechnician
from plotter import Plotter

def get_num_technicians():
    """Získanie počtu technikov od užívateľa."""
    while True:
        try:
            num_technicians = int(input("Zadaj počet technikov: "))
            if num_technicians < 1:
                print("Počet technikov musí byť väčší alebo rovný 1.")
            else:
                return num_technicians
        except ValueError:
            print("Zadaj platné celé číslo.")

def get_simulate_breaks():
    """Zisťuje, či chceme simulovať prestávky."""
    while True:
        simulate_breaks_input = input("Chceš simulovať prestávky pre technikov? (y/n): ").strip().lower()
        if simulate_breaks_input in ['y', 'n']:
            return simulate_breaks_input == "y"
        else:
            print("Neplatná voľba. Zadaj 'y' alebo 'n'.")

def manual_run():
    """Manuálny beh simulácie laboratória."""
    num_technicians = get_num_technicians()
    simulate_breaks = get_simulate_breaks()

    # Vytvorenie systému so zadaným počtom technikov a nastavením pre simuláciu prestávok
    system = LabSystem(num_technicians, simulate_breaks)
    system.generate_samples()  # Generovanie vzoriek
    system.simulate_day()  # Simulácia dňa
    total, on_time = system.collect_stats()  # Získanie štatistík

    print(f"Technikov: {num_technicians}")
    for i in range(3):
        print(f"Kategória {i + 1}: {on_time[i]}/{total[i]} načas ({on_time[i] / total[i] * 100:.2f}%)")

    all_samples = sum(total)
    late = all_samples - sum(on_time)
    print(f"Vzorky neskoro: {late}/{all_samples} = {late / all_samples * 100:.2f}%")

    # Vykreslíme grafy, len pri manuálnom behu
    system.plotter.plot_waiting_samples()
    system.plotter.plot_sample_categories_pie()
    system.plotter.plot_average_waiting_samples()
    system.plotter.plot_on_time_vs_late_samples()

    # Vyžiadanie vyťaženosti technikov
    utilization = system.get_utilization()
    for i, util in enumerate(utilization, 1):
        print(f"Tech_{i} vyťaženosť: {util * 100:.2f}%")

    # Uloženie dát do CSV
    system.save_data_to_csv()

def run_experiment():
    """Experiment na určenie minimálneho počtu technikov potrebného na dosiahnutie cieľa <= 3% neskoro."""
    min_technicians = 1
    max_technicians = 50
    target_late_ratio = 0.03

    plot_graphs = input("Chceš po experimente zobraziť grafy? (y/n): ").lower() == 'y'

    for num_technicians in range(min_technicians, max_technicians + 1):
        system = LabSystem(num_technicians)
        system.generate_samples()
        system.simulate_day()
        total, on_time = system.collect_stats()
        late_ratio = system.get_late_ratio()

        if late_ratio <= target_late_ratio:
            print(f"Technikov: {num_technicians}, Priemerné % neskoro: {late_ratio * 100:.2f}%")
            print(f"✅ Najmenší počet technikov s <= 3% oneskorením: {num_technicians}")

            print("\n📊 Vyťaženosť technikov:")
            for tech in system.technicians:
                utilization = min(tech.busy_time, 240) / 240  # 240 minútový pracovný čas (7:00 - 11:00)
                print(f"{tech.name}: {utilization * 100:.2f}%")

            system.save_data_to_csv()
            if plot_graphs:
                # Po nájdení optimálneho počtu technikov, zobraz grafy
                system.plotter.plot_waiting_samples()
                system.plotter.plot_average_waiting_samples()
                system.plotter.plot_on_time_vs_late_samples()
                system.plotter.plot_sample_categories_pie()

            break

def main():
    """Hlavná funkcia na výber simulácie alebo experimentu."""
    print("Vyber možnosť:")
    print("1 - Manuálny beh simulácie (zadaj počet technikov)")
    print("2 - Experiment na zistenie minimálneho počtu technikov (≤ 3% neskoro)")

    choice = input("Tvoja voľba: ")

    if choice == "1":
        manual_run()
    elif choice == "2":
        run_experiment()
    else:
        print("Neplatná voľba.")

if __name__ == "__main__":
    main()
