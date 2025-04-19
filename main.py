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



def run_experiment():
    min_technicians = 1
    max_technicians = 50  # Určíme max počet technikov pre testovanie
    target_late_ratio = 0.03  # 3% oneskorených vzoriek

    for num_technicians in range(min_technicians, max_technicians + 1):
        system = LabSystem(num_technicians)
        system.generate_samples()
        system.simulate_day()
        total, on_time = system.collect_stats()

        late_ratio = system.get_late_ratio()

        # Ak neskoro spracovaných vzoriek je ≤ 3%, experiment skončí
        if late_ratio <= target_late_ratio:
            print(f"Technikov: {num_technicians}, Priemerné % neskoro: {late_ratio * 100:.2f}%")
            print(f"✅ Najmenší počet technikov s <= 3% oneskorením: {num_technicians}")
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
