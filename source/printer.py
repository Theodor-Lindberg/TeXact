"""Class for printing output."""

from typing import TYPE_CHECKING

from colorama import Fore, Style, init as colorama_init

if TYPE_CHECKING:  # Only for type hints
    from reviewer import Status


class Printer:
    GREEN = Fore.GREEN
    DARK_RED = Fore.RED
    YELLOW = Fore.YELLOW
    RESET = Style.RESET_ALL

    def __init__(self) -> None:
        colorama_init()

    def print(self, message: str) -> None:
        print(message)

    def print_no(self, line_no: int, message: str) -> None:
        line_no = f"L{line_no + 1}:"
        print(f"{self.green(line_no)} {message}")

    def green(self, message: str) -> str:
        return f"{self.GREEN}{message}{self.RESET}"

    def yellow(self, message: str) -> str:
        return f"{self.YELLOW}{message}{self.RESET}"

    def dark_red(self, message: str) -> str:
        return f"{self.DARK_RED}{message}{self.RESET}"

    def status_str(self, status: "Status") -> str:
        name = getattr(status, "name", str(status))
        if name == "PASSED":
            return self.green(name)
        elif name == "FAILED":
            return self.dark_red(name)
        else:
            return self.yellow(name)
