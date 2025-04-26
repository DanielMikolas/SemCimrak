
class LabTechnician:
    def __init__(self, name):
        self.name = name
        self.busy_until = 0  # čas do kedy je zaneprázdnený
        self.samples_processed = []
        self.busy_time = 0

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
