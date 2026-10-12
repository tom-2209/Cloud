

class Process:
    def __init__(self, pid, n):
        self.pid = pid
        self.vector = [0] * n

    def event(self):
        self.vector[self.pid] += 1
        print(f"P{self.pid + 1}: Internal event, Vector = {self.vector}")

    def send_message(self):
        self.vector[self.pid] += 1
        message = self.vector.copy()
        print(f"P{self.pid + 1}: Sending message, Vector = {message}")
        return message

    def receive_message(self, message):
        for i in range(len(self.vector)):
            self.vector[i] = max(self.vector[i], message[i])

        self.vector[self.pid] += 1
        print(f"P{self.pid + 1}: Received message, Vector = {self.vector}")


# Create three processes
p1 = Process(0, 3)
p2 = Process(1, 3)
p3 = Process(2, 3)

# Internal events
p1.event()
p2.event()

# P1 sends a message to P2
message = p1.send_message()

# P2 receives the message
p2.receive_message(message)

# P3 performs an independent event
p3.event()

# P2 sends a message to P3
message = p2.send_message()
p3.receive_message(message)
