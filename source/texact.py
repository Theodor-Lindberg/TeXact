import argparse

from pathlib import Path
from printer import Printer
from rewiever_ould import Reviewer_ould
from reviewer_inthis import Reviewer_Inthis
from reviewer_reflabel import Reviewer_RefLabel
from reviewer_casing import Reviewer_Casing
from reviewer_figure import Reviewer_Figure


def set_up_arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automated LaTeX reviewer(s). Can you pass the judgement?"
    )
    parser.add_argument(
        "-f", "--file", required=True, type=str, help="Path to the LaTeX file"
    )
    parser.add_argument(
        "--ould",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Find should|would|could",
    )
    return parser.parse_args()


def process_file(file_path: Path, reviewers: tuple, printer: Printer) -> int:
    with file_path.open("r", encoding="utf-8") as input_file:
        for line_no, line in enumerate(input_file):
            for reviewer in reviewers:
                reviewer.process_line(line_no, line)

    all_comments: list[tuple[int, str]] = []
    for reviewer in reviewers:
        all_comments.extend(reviewer.get_comments())

    for line_no, message in sorted(all_comments, key=lambda comment: comment[0]):
        printer.print_no(line_no, message)

    printer.print("=== Summary ===")
    for reviewer in reviewers:
        name = reviewer.get_name()
        status = printer.status_str(reviewer.get_status())
        summary = reviewer.get_summary()
        printer.print(f"Reviewer {name}: {status}. {summary}")


def main():
    args = set_up_arg_parser()
    file_path = Path(args.file)
    printer = Printer()

    if not file_path.is_file():
        raise SystemExit(
            f"Error: '{file_path}' does not exist or is not a regular file."
        )

    # Add reviewers
    reviewers = [
        Reviewer_Inthis(printer),
        Reviewer_RefLabel(printer),
        Reviewer_Casing(printer),
        Reviewer_Figure(printer),
    ]
    if args.ould:
        reviewers.append(Reviewer_ould(printer))

    process_file(file_path, tuple(reviewers), printer)


if __name__ == "__main__":
    main()
