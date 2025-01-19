from abc import abstractmethod
from queue import Empty, Queue
from threading import Event, Thread

from app.devices.io.io_process import IoProcess, T


class IoWriteProcess(IoProcess[T]):
    def __init__(self, queue: Queue[T]) -> None:
        self._process = Thread(target=self._run, args=(queue,))
        self._exit_event = Event()
        self.poll_interval = 0.1

    def _run(self, queue: Queue[T]) -> None:
        self.first_tick()
        while not self._exit_event.is_set():
            try:
                self.tick(queue.get(True, self.poll_interval))
            except Empty:
                pass

    @abstractmethod
    def first_tick(self) -> None:
        pass

    @abstractmethod
    def tick(self, data: T) -> None:
        pass

    def start(self) -> None:
        self._process.start()

    def stop(self) -> None:
        self._exit_event.set()
        self._process.join()
