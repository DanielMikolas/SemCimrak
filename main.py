from LabSystem import LabSystem
from Experiment import Experiment
from plotter import Plotter  # Importujeme triedu Plotter


def manual_run():
    try:
        num_technicians = int(input("Zadaj počet technikov: "))
    except ValueError:
        print("Zadaj platné celé číslo.")
        return

    system = LabSystem(num_technicians)
    system.generate_samples()
    system.simulate_day()
    total, on_time = system.collect_stats()

    print(f"Technikov: {num_technicians}")
    for i in range(3):
        print(f"Kategória {i + 1}: {on_time[i]}/{total[i]} načas ({on_time[i] / total[i] * 100:.2f}%)")

    all_samples = sum(total)
    late = all_samples - sum(on_time)
    print(f"Vzorky neskoro: {late}/{all_samples} = {late / all_samples * 100:.2f}%")

    # Tu sa vykreslí graf len pri manuálnom behu
    system.plotter.plot_waiting_samples()
    system.plotter.plot_sample_categories_pie()
    system.plotter.plot_average_waiting_samples()
    system.plotter.plot_on_time_vs_late_samples()

    utilization = system.get_utilization()
    for i, util in enumerate(utilization, 1):
        print(f"Tech_{i} vyťaženosť: {util * 100:.2f}%")

    system.save_data_to_csv()
#
# def run_experiment():
#     min_technicians = 1
#     max_technicians = 50
#     target_late_ratio = 0.03
#
#     for num_technicians in range(min_technicians, max_technicians + 1):
#         system = LabSystem(num_technicians)
#         system.generate_samples()
#         system.simulate_day()
#         total, on_time = system.collect_stats()
#         late_ratio = system.get_late_ratio()
#
#         if late_ratio <= target_late_ratio:
#             print(f"Technikov: {num_technicians}, Priemerné % neskoro: {late_ratio * 100:.2f}%")
#             print(f"✅ Najmenší počet technikov s <= 3% oneskorením: {num_technicians}")
#
#             print("\n📊 Vyťaženosť technikov:")
#             for tech in system.technicians:
#                 utilization = min(tech.busy_time, 240) / 240  # 240 minútový pracovný čas (7:00 - 11:00)
#                 print(f"{tech.name}: {utilization * 100:.2f}%")
#
#             system.save_data_to_csv()
#             break
#
#
#
#
def run_experiment():
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
            # 🆕 Po nájdení optimálneho počtu technikov, zobraz grafy:
                system.plotter.plot_waiting_samples()
                system.plotter.plot_average_waiting_samples()
                system.plotter.plot_on_time_vs_late_samples()
                system.plotter.plot_sample_categories_pie()

            break

def main():
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