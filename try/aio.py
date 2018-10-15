
import asyncio
import time
from typing import List


class SomethingThatWaits:
    def __init__(self, timeout_in_sec: int = 3) -> None:
        self.timeout_in_sec = timeout_in_sec
        self.check_interval_in_sec = 1

        self.last_heard = time.monotonic()

    async def start(self) -> None:
        while True:
            await asyncio.sleep(self.check_interval_in_sec)
            current_time = time.monotonic()
            elapsed_in_sec = current_time - self.last_heard
            print('checking', elapsed_in_sec)
            if elapsed_in_sec >= self.timeout_in_sec:
                print('I timed out!!')
                raise TimeoutError('timed out!')

    def receive_heartbeat(self) -> None:
        self.last_heard = time.monotonic()


class SomethingThatSends:
    def __init__(self, heartbeat_interval: int = 1) -> None:
        self.heartbeat_interval = heartbeat_interval

    async def send_heartbeat(self, waiter_list: List['SomethingThatWaits']) -> None:
        # while True:
        for ix in range(3):
            await asyncio.sleep(self.heartbeat_interval)
            for waiter in waiter_list:
                waiter.receive_heartbeat()


waiter1 = SomethingThatWaits(timeout_in_sec=10)
waiter2 = SomethingThatWaits(timeout_in_sec=6)
sender1 = SomethingThatSends(heartbeat_interval=5)

loop = asyncio.new_event_loop()

tasks = [
    waiter1.start(),
    waiter2.start(),
    sender1.send_heartbeat([waiter1, waiter2]),
]

start = time.monotonic()
loop.run_until_complete(asyncio.wait(tasks))  # FIXME: figure out the exception handling for this

end = time.monotonic()
print(end - start)
