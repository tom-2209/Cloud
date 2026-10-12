### CENTRALIZED Code

import threading
import queue
import time

requests = queue.Queue()
cs_lock = threading.Lock()

def coordinator():
    while True:
        item = requests.get()
        if item is None:
            break

        pid, reply = item
        reply.put("GRANT")
        release_event = reply.get()

        if release_event == "RELEASE":
            print(f"Coordinator: P{pid} released CS")

def process(pid):
    reply = queue.Queue()

    print(f"P{pid}: REQUEST")
    requests.put((pid, reply))
    reply.get()

    with cs_lock:
        print(f"P{pid}: ENTER CS")
        time.sleep(1)
        print(f"P{pid}: EXIT CS")

    reply.put("RELEASE")
    print(f"P{pid}: RELEASE sent")

threading.Thread(target=coordinator, daemon=True).start()

workers = []
for pid in [1, 2, 3]:
    t = threading.Thread(target=process, args=(pid,))
    workers.append(t)
    t.start()

for t in workers:
    t.join()

requests.put(None)
print("Centralized algorithm completed")


### Ricart Algorithm
import threading
import queue
import time

N = 3
inboxes = [queue.Queue() for _ in range(N)]
states = ["RELEASED"] * N
clock = [0] * N
request_time = [0] * N
replies = [0] * N
deferred = [set() for _ in range(N)]
locks = [threading.Lock() for _ in range(N)]
conditions = [threading.Condition(locks[i]) for i in range(N)]

def receiver(pid):
    while True:
        msg = inboxes[pid].get()

        if msg[0] == "STOP":
            break

        kind, other, timestamp = msg

        if kind == "REQUEST":
            clock[pid] = max(clock[pid], timestamp) + 1

            with conditions[pid]:
                my_priority = (request_time[pid], pid)
                other_priority = (timestamp, other)

                if (states[pid] == "RELEASED"
                    or (states[pid] == "REQUESTING"
                        and other_priority < my_priority)):
                    inboxes[other].put(("REPLY", pid, clock[pid]))
                else:
                    deferred[pid].add(other)

        elif kind == "REPLY":
            with conditions[pid]:
                replies[pid] += 1
                conditions[pid].notify_all()

def request_cs(pid):
    with conditions[pid]:
        clock[pid] += 1
        request_time[pid] = clock[pid]
        states[pid] = "REQUESTING"
        replies[pid] = 0
        timestamp = request_time[pid]

    print(f"P{pid}: REQUEST sent")
    for other in range(N):
        if other != pid:
            inboxes[other].put(("REQUEST", pid, timestamp))

    with conditions[pid]:
        while replies[pid] < N - 1:
            conditions[pid].wait()
        states[pid] = "HELD"

    print(f"P{pid}: ENTER CS")
    time.sleep(1)
    print(f"P{pid}: EXIT CS")

    with conditions[pid]:
        states[pid] = "RELEASED"
        waiting = list(deferred[pid])
        deferred[pid].clear()

    for other in waiting:
        inboxes[other].put(("REPLY", pid, clock[pid]))

for pid in range(N):
    threading.Thread(target=receiver, args=(pid,), daemon=True).start()

workers = []
for pid in range(N):
    t = threading.Thread(target=request_cs, args=(pid,))
    workers.append(t)
    t.start()
    time.sleep(0.1)

for t in workers:
    t.join()

for inbox in inboxes:
    inbox.put(("STOP", 0, 0))

print("Ricart-Agrawala completed")


#Token Algorithm
import threading
import queue
import time

N = 3
token_queues = [queue.Queue() for _ in range(N)]
token_queues[0].put("TOKEN")

def process(pid):
    for turn in range(2):
        token = token_queues[pid].get()

        print(f"P{pid}: Received token")

        # Demonstrate a request to enter CS
        print(f"P{pid}: REQUEST CS")
        print(f"P{pid}: ENTER CS")
        time.sleep(0.5)
        print(f"P{pid}: EXIT CS")

        next_pid = (pid + 1) % N
        print(f"P{pid}: Passing token to P{next_pid}")
        token_queues[next_pid].put(token)

threads = []
for pid in range(N):
    t = threading.Thread(target=process, args=(pid,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Token Ring completed")

