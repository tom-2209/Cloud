
class Process:
    def __init__(self, pid):
        self.pid = pid
        self.clock = 0

    def event(self):
        self.clock += 1
        print(f"Process P{self.pid}: Internal event, Clock = {self.clock}")

    def send_message(self):
        self.clock += 1
        timestamp = self.clock
        print(f"Process P{self.pid}: Sending message, Timestamp = {timestamp}")
        return timestamp

    def receive_message(self, timestamp):
        self.clock = max(self.clock, timestamp) + 1
        print(f"Process P{self.pid}: Received message, Clock = {self.clock}")


# Create two distributed processes
p1 = Process(1)
p2 = Process(2)

# Internal events
p1.event()
p2.event()

# P1 sends a message to P2
timestamp = p1.send_message()

# P2 receives the message
p2.receive_message(timestamp)

# More events
p1.event()
p2.event()
