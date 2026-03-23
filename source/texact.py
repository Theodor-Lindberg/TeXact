import argparse

from pathlib import Path
from printer import Printer
from rewiever_ould import Reviewer_ould


def set_up_arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automated LaTeX reviewer(s). Can you pass the judgement?")
    parser.add_argument("-f", "--file", required=True, type=str, help="Path to the LaTeX file")
    parser.add_argument("--ould", default=True, type=bool, help="Find should|would|could")
    return parser.parse_args()


def process_file(file_path: Path, reviewers: tuple) -> int:
    with file_path.open("r", encoding="utf-8") as input_file:
        for line_no, line in enumerate(input_file):
            for reviewer in reviewers:
                reviewer.process_line(line_no, line)

    for reviewer in reviewers:
        reviewer.summarize()


def main():
    args = set_up_arg_parser()
    file_path = Path(args.file)
    printer = Printer()

    if not file_path.is_file():
        raise SystemExit(f"Error: '{file_path}' does not exist or is not a regular file.")
    
    # Add reviewers
    reviewers = []
    if args.ould:
        reviewers.append(Reviewer_ould(printer))

    process_file(file_path, tuple(reviewers))
    #print(f"ould-count: {match_count}")


if __name__ == "__main__":
    main()