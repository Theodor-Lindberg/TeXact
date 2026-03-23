"""
Class for printing output.
"""

class Printer:
    GREEN = "\033[32m"
    DARK_RED = "\033[38;5;88m"
    RESET = "\033[0m"

    def print(self, message: str) -> None:
        print(message)

    def print_no(self, line_no: int, message: str) -> None:
        line_no = f"{line_no+1}:"
        print(f"{self.green(line_no)}{message}")

    def green(self, message: str) -> str:
        return f"{self.GREEN}{message}{self.RESET}"

    def dark_red(self, message: str) -> str:
        return f"{self.DARK_RED}{message}{self.RESET}"