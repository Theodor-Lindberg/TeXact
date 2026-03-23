import re

from reviewer import Reviewer, Status
from printer import Printer


class Reviewer_Figure(Reviewer):
    _PATTERN_BEGIN_FIGURE = re.compile(r"\\begin\{figure")
    _PATTERN_END_FIGURE = re.compile(r"\\end\{figure")
    _PATTERN_INCLUDEGRAPHICS = re.compile(r"\\includegraphics\s*(?:\[[^\]]*\])?")
    _PATTERN_SCALE = re.compile(r"(?:scale|width|height)\s*=", re.IGNORECASE)
    _PATTERN_LABEL = re.compile(r"\\label\{")
    _PATTERN_CAPTION = re.compile(r"\\caption(?:\[[^\]]*\])?\{")
    _PATTERN_CAPTION_CONTENT = re.compile(r"\\caption(?:\[[^\]]*\])?\{([^}]*)\}")

    def __init__(self, printer: Printer) -> None:
        self.printer = printer
        self.comments: list[tuple[int, str]] = []
        self.error_count = 0
        
        # Track figure environment state
        self.in_figure = False
        self.figure_start_line = -1
        self.has_label_in_figure = False
        self.has_caption_in_figure = False
        self.has_scaled_image_in_figure = False
        self.first_caption_line: int | None = None
        self.first_includegraphics_line: int | None = None
        self.includegraphics_lines: list[int] = []
        self.caption_period_style: bool | None = None
        self.caption_period_all_same = True
        self.caption_period_issue_line: int | None = None
        self.caption_period_issue_added = False

    def process_line(self, line_no: int, line: str) -> None:
        # Remove comments (everything after %)
        if "%" in line:
            line = line[:line.index("%")]

        # Check for figure environment start
        if self._PATTERN_BEGIN_FIGURE.search(line):
            self.in_figure = True
            self.figure_start_line = line_no
            self.has_label_in_figure = False
            self.has_caption_in_figure = False
            self.has_scaled_image_in_figure = False
            self.first_caption_line = None
            self.first_includegraphics_line = None
            self.includegraphics_lines = []

        if self.in_figure:
            # Check for label
            if self._PATTERN_LABEL.search(line):
                self.has_label_in_figure = True

            if self._PATTERN_CAPTION.search(line):
                self.has_caption_in_figure = True
                if self.first_caption_line is None:
                    self.first_caption_line = line_no
                caption_match = self._PATTERN_CAPTION_CONTENT.search(line)
                if caption_match:
                    caption_text = caption_match.group(1).strip()
                    caption_has_period = caption_text.endswith(".")
                    if self.caption_period_style is None:
                        self.caption_period_style = caption_has_period
                    elif caption_has_period != self.caption_period_style:
                        self.caption_period_all_same = False
                        if self.caption_period_issue_line is None:
                            self.caption_period_issue_line = line_no

            # Check for includegraphics
            if self._PATTERN_INCLUDEGRAPHICS.search(line):
                self.includegraphics_lines.append(line_no)
                if self.first_includegraphics_line is None:
                    self.first_includegraphics_line = line_no
                # Check if image is scaled
                if self._PATTERN_SCALE.search(line):
                    self.has_scaled_image_in_figure = True
                    self.comments.append(
                        (
                            line_no,
                            f"Image should not be scaled: {self.printer.dark_red('remove scale/width/height')}"
                        )
                    )
                    self.error_count += 1

        # Check for figure environment end
        if self._PATTERN_END_FIGURE.search(line):
            if self.in_figure:
                # Report missing label if there's an image
                if self.includegraphics_lines and not self.has_label_in_figure:
                    self.comments.append(
                        (
                            self.figure_start_line,
                            f"Figure environment should contain a {self.printer.dark_red('\\\\label{{...}}')}"
                        )
                    )
                    self.error_count += 1

                if self.includegraphics_lines and not self.has_caption_in_figure:
                    self.comments.append(
                        (
                            self.figure_start_line,
                            f"Figure environment should contain a {self.printer.dark_red('\\\\caption{{...}}')}"
                        )
                    )
                    self.error_count += 1

                if (
                    self.first_caption_line is not None
                    and self.first_includegraphics_line is not None
                    and self.first_caption_line < self.first_includegraphics_line
                ):
                    self.comments.append(
                        (
                            self.first_caption_line,
                            "Figure caption should be below the graphics."
                        )
                    )
                    self.error_count += 1

            self.in_figure = False
            self.figure_start_line = -1
            self.has_label_in_figure = False
            self.has_caption_in_figure = False
            self.has_scaled_image_in_figure = False
            self.first_caption_line = None
            self.first_includegraphics_line = None
            self.includegraphics_lines = []

    def get_comments(self) -> list[tuple[int, str]]:
        self._add_caption_period_consistency_issue()
        return self.comments

    def _add_caption_period_consistency_issue(self) -> None:
        if self.caption_period_issue_added:
            return

        if self.caption_period_all_same:
            return

        issue_line = self.caption_period_issue_line if self.caption_period_issue_line is not None else 0
        self.comments.append(
            (
                issue_line,
                "Caption period style mismatch: all figure captions should use the same period style."
            )
        )
        self.error_count += 1
        self.caption_period_issue_added = True

    def get_summary(self) -> str:
        if self.error_count == 0:
            return ""
        return f"figure-errors: {self.error_count}"

    def get_status(self) -> Status:
        return Status.PASSED if self.error_count == 0 else Status.FAILED

    def get_name(self) -> str:
        return "Figure"
