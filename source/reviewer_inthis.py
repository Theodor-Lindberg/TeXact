import re

from reviewer import Reviewer, Status
from printer import Printer


class Reviewer_Inthis(Reviewer):
    _PATTERN_ABSTRACT_START = re.compile(r"\\begin\{abstract\}")
    _PATTERN_CONCLUSIONS_START = re.compile(r"\\section\{Conclusion", re.IGNORECASE)
    _PATTERN_THIS_WORK = re.compile(
        r"\bthis\s+(?:\w+\s+)*(work|brief|paper|manuscript)s?\b",
        re.IGNORECASE,
    )

    def __init__(self, printer: Printer) -> None:
        self.printer = printer
        self.abstract_context_start = False
        self.check_abstract_first_line = False
        self.conclusions_context_start = False
        self.check_conclusions_first_line = False
        self.abstract_check = Status.UNCHECKED
        self.conclusions_check = Status.UNCHECKED

    def process_line(self, line_no: int, line: str) -> None:
        if self.abstract_check == Status.UNCHECKED:
            if self._PATTERN_ABSTRACT_START.search(line):
                self.check_abstract_first_line = True
                return

        if self.check_abstract_first_line:
            if line and line[0] != '%': # Skip empty lines and comments
                self.check_abstract_first_line = False
                if self._PATTERN_THIS_WORK.search(line):
                    self.abstract_check = Status.FAILED
                    self.printer.print_no(
                        line_no,
                        "First line in abstract should not contain 'in this work/brief/paper/manuscript' or 'this paper'.",
                    )
                else:
                    self.abstract_check = Status.PASSED

        if self.conclusions_check == Status.UNCHECKED:
            if self._PATTERN_CONCLUSIONS_START.search(line):
                self.check_conclusions_first_line = True
                return

        if self.check_conclusions_first_line:
            if line and line[0] != '%': # Skip empty lines and comments
                self.check_conclusions_first_line = False
                if self._PATTERN_THIS_WORK.search(line):
                    self.conclusions_check = Status.FAILED
                    self.printer.print_no(
                        line_no,
                        "First line in conclusions should not contain 'in this work/brief/paper/manuscript' or 'this paper'.",
                    )
                else:
                    self.conclusions_check = Status.PASSED


    def get_summary(self) -> str:
        return ""

    def get_status(self) -> Status:
        if self.abstract_check == Status.PASSED and self.conclusions_check == Status.PASSED:
            return Status.PASSED
        elif self.abstract_check == Status.FAILED or self.conclusions_check == Status.FAILED:
            return Status.FAILED
        else:
            return Status.UNCHECKED
        
    def get_name(self) -> str:
        return "InThisWork"