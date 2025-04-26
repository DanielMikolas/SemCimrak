import random
class LabTechnician:
    def __init__(self, name):
        self.name = name
        self.busy_until = 0  # čas do kedy je zaneprázdnený
        self.samples_processed = []
        self.busy_time = 0
       # self.work_time_since_break = 0  # koľko minút pracuje bez prestávky

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


        #pridana simulacia prestavok pacienta
        # self.work_time_since_break += process_duration

        #Kontrola, či si technik potrebuje dať prestávku

        # if self.work_time_since_break >= 90:  # ak odpracoval viac ako 90 minút bez prestávky
        #     if random.random() < 0.5:  # 50% šanca, že si prestávku dá
        #         break_duration = random.randint(5, 10)  # prestávka 5-10 minút
        #         self.busy_until += break_duration  # posun busy_until o prestávku
        #         self.work_time_since_break = 0  # resetujeme počítadlo