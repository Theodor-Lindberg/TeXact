import re

from reviewer import Reviewer, Status
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

    def get_summary(self) -> str:
        return f"ould-count: {self.match_count}"

    def get_status(self) -> Status:
        return Status.PASSED if self.match_count == 0 else Status.FAILED

    def find_ould(self, line: str) -> list[str]:
        return self._PATTERN.findall(line)
    
    def get_name(self) -> str:
        return "Ould"