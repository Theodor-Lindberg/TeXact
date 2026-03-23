from abc import ABC, abstractmethod

from printer import Printer


class Reviewer(ABC):
    @abstractmethod
    def __init__(self, printer: Printer) -> None:
        raise NotImplementedError

    @abstractmethod
    def process_line(self, line_no: int, line: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def summarize(self) -> None:
        raise NotImplementedError