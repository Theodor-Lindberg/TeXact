import re

from reviewer import Reviewer, Status
from printer import Printer


class Reviewer_Casing(Reviewer):
    # Dictionary mapping lowercase versions to correct spellings
    CORRECT_SPELLINGS = {
        "asic": "ASIC",
        "fpga": "FPGA",
        "vlsi": "VLSI",
        "flopoco": "FloPoCo",
        "ai": "AI",
        "ml": "ML",
    }

    def __init__(self, printer: Printer) -> None:
        self.printer = printer
        self.comments: list[tuple[int, str]] = []
        self.mismatch_count = 0

    def process_line(self, line_no: int, line: str) -> None:
        # Remove comments (everything after %)
        if "%" in line:
            line = line[:line.index("%")]

        # Check each word in the line
        for word_lower, correct_spelling in self.CORRECT_SPELLINGS.items():
            # Create regex pattern to find case-insensitive matches with word boundaries
            pattern = re.compile(r"\b" + re.escape(word_lower) + r"\b", re.IGNORECASE)
            
            for match in pattern.finditer(line):
                matched_text = match.group(0)
                # If the matched text doesn't match the correct spelling exactly
                if matched_text != correct_spelling:
                    self.comments.append(
                        (
                            line_no,
                            f"Incorrect casing: {self.printer.dark_red(matched_text)} should be {self.printer.yellow(correct_spelling)}"
                        )
                    )
                    self.mismatch_count += 1

    def get_comments(self) -> list[tuple[int, str]]:
        return self.comments

    def get_summary(self) -> str:
        if self.mismatch_count == 0:
            return ""
        return f"Casing errors: {self.mismatch_count}"

    def get_status(self) -> Status:
        return Status.PASSED if self.mismatch_count == 0 else Status.FAILED

    def get_name(self) -> str:
        return "Casing"
