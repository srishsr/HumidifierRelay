from abc import abstractmethod
from queue import Queue
from threading import Event, Thread

from app.devices.io.io_process import IoProcess, T


class IoReadProcess(IoProcess[T]):
    def __init__(self, queue: Queue[T]) -> None:
        self.queue = queue
        self._process = Thread(target=self._run, args=(queue,), daemon=True)
        self._exit_event = Event()

    def _run(self, queue: Queue[T]) -> None:
        self.first_tick()
        while not self._exit_event.is_set():
            next_data = self.tick()
            if next_data is not None:
                queue.put(next_data)

    @abstractmethod
    def first_tick(self) -> None:
        pass

    @abstractmethod
    def tick(self) -> T:
        pass

    def start(self) -> None:
        self._process.start()

    def get(self) -> T | None:
        if self.queue.empty():
            return None
        return self.queue.get()

    def stop(self) -> None:
        self._exit_event.set()
