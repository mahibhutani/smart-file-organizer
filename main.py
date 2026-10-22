
"""Command-line interface for the Smart File Organizer."""

import argparse

from organizer import FileOrganizer


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organize files by extension."
    )
    parser.add_argument(
        "--source",
        default=".",
        help="Directory to organize (default: current directory).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move files. Without this flag, preview only.",
    )

    args = parser.parse_args()

    try:
        organizer = FileOrganizer(args.source)
        actions = organizer.organize(apply=args.apply)
    except (NotADirectoryError, PermissionError, OSError) as error:
        parser.error(str(error))

    if not actions:
        print("No files found to organize.")
        return

    if not args.apply:
        print("DRY RUN: no files have been moved.")
    else:
        print(f"Completed {len(actions)} file move(s).")

    for action in actions:
        print(f"{action.source.name} -> {action.destination}")


if __name__ == "__main__":
    main()
