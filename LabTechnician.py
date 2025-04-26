import random

class LabTechnician:
    """
    Trieda reprezentujúca technika v laboratóriu, ktorý spracováva vzorky.
    Technici môžu mať prestávky, ktoré ovplyvňujú ich dostupnosť.
    """

    def __init__(self, name, simulate_breaks=False):
        """
        Inicializácia technika.

        :param name: Meno technika.
        :param simulate_breaks: Určuje, či sa simulujú prestávky.
        """
        self.name = name
        self.busy_until = 0  # Čas do kedy je technik zaneprázdnený
        self.samples_processed = []  # Zoznam spracovaných vzoriek
        self.busy_time = 0  # Celkový čas, počas ktorého bol technik zaneprázdnený
        self.simulate_breaks = simulate_breaks  # Ak je True, technik bude mať prestávky
        self.work_time_since_break = 0  # Čas, ktorý technik pracuje od poslednej prestávky

    def is_available(self, current_time):
        """
        Skontroluje, či je technik dostupný na spracovanie ďalšej vzorky.

        :param current_time: Aktuálny čas simulácie.
        :return: True, ak je technik dostupný, inak False.
        """
        return current_time >= self.busy_until

    def process_sample(self, sample, current_time, process_duration):
        """
        Spracuje vzorku, nastaví časy a aktualizuje stav technika.

        :param sample: Vzorka, ktorá sa má spracovať.
        :param current_time: Aktuálny čas simulácie.
        :param process_duration: Doba spracovania vzorky v minútach.
        """
        sample.start_time = current_time  # Nastavenie času začiatku spracovania
        sample.process_time = process_duration  # Doba spracovania vzorky
        sample.completed_time = current_time + process_duration  # Čas, kedy bude vzorka dokončená
        # Určí, či bola vzorka spracovaná načas
        sample.completed_in_time = (sample.completed_time - sample.arrival_time <= sample.deadline_minutes)

        # Nastavenie času, kedy bude technik opäť dostupný
        self.busy_until = sample.completed_time
        self.samples_processed.append(sample)  # Pridanie spracovanej vzorky do zoznamu
        self.busy_time += process_duration  # Aktualizácia celkového času zaneprázdnenia technika
        self.work_time_since_break += process_duration  # Pridanie času spracovania k práci bez prestávky

        # Simulácia prestávok pre technika
        if self.simulate_breaks and self.work_time_since_break >= 90:  # Ak technik pracuje viac ako 90 minút
            if random.random() < 0.5:  # 50% šanca, že si technik dá prestávku
                break_duration = random.randint(5, 10)  # Prestávka medzi 5 a 10 minútami
                self.busy_until += break_duration  # Posúvame čas, kedy bude technik opäť k dispozícii
                self.work_time_since_break = 0  # Resetujeme čas od poslednej prestávky
