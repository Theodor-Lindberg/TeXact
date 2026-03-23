import re

from reviewer import Reviewer, Status
from printer import Printer


class Reviewer_ould(Reviewer):
    _PATTERN = re.compile(r"\b(?:should|would|could)\b", re.IGNORECASE)

    def __init__(self, printer: Printer) -> None:
        self.printer = printer
        self.match_count = 0
        self.comments: list[tuple[int, str]] = []

    def process_line(self, line_no: int, line: str) -> None:
        matches = self.find_ould(line)
        if matches:
            message = self._PATTERN.sub(
                lambda match: self.printer.dark_red(match.group(0)),
                line.rstrip("\n"),
            )
            self.comments.append((line_no, message))
            self.match_count += len(matches)

    def get_comments(self) -> list[tuple[int, str]]:
        return self.comments

    def get_summary(self) -> str:
        if not self.match_count:
            return ""
        else:
            return f"ould-count: {self.match_count}"

    def get_status(self) -> Status:
        return Status.PASSED if self.match_count == 0 else Status.FAILED

    def find_ould(self, line: str) -> list[str]:
        return self._PATTERN.findall(line)
    
    def get_name(self) -> str:
        return "Ould"