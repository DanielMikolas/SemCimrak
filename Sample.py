class Sample:
    def __init__(self, arrival_time, category, deadline_minutes):
        self.arrival_time = arrival_time            # minúta medzi 0 (7:00) a 120 (9:00)
        self.category = category                    # 1, 2 alebo 3
        self.deadline_minutes = deadline_minutes    # 20, 60 alebo 180
        self.start_time = None                      # kedy sa začalo spracovanie
        self.process_time = None                    # dĺžka spracovania (5–9 min)
        self.completed_time = None                  # čas ukončenia
        self.completed_in_time = None               # boolean
