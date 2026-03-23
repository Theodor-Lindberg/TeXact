import re

from reviewer import Reviewer
from printer import Printer


class Reviewer_ould(Reviewer):
    _PATTERN = re.compile(r"\b(?:should|would|could)\b", re.IGNORECASE)

    def __init__(self, printer: Printer) -> None:
        self.printer = printer
        self.match_count = 0

    def process_line(self, line_no: int, line: str) -> None:
        matches = self.find_ould(line)
        if matches:
            message = self._PATTERN.sub(
                lambda match: self.printer.dark_red(match.group(0)),
                line.rstrip("\n"),
            )
            self.printer.print_no(line_no, message)
            self.match_count += len(matches)

    def summarize(self) -> None:
        self.printer.print(f"ould-count: {self.match_count}")

    def find_ould(self, line: str) -> list[str]:
        return self._PATTERN.findall(line)