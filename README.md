<<<<<<< HEAD

# Smart File Organizer

A Python command-line utility that organizes files into folders based on
their extensions. It supports preview mode, duplicate filename handling,
and basic error reporting.

## Features

- Categorizes images, documents, videos, audio, archives, and code files.
- Places unrecognized file types in an Others folder.
- Previews planned moves without changing files by default.
- Avoids intentionally overwriting existing destination files.
- Skips directories and symbolic links.
- Includes automated tests using pytest.

## Requirements

- Python 3.10 or newer
- pytest (for running tests)

## Setup

Clone the repository, then open a terminal in the project directory.

Install the testing dependency:

    python -m pip install -r requirements.txt

## Usage

Preview the organization of a test directory:

    python main.py --source "./sample-files"

Apply the moves after checking the preview:

    python main.py --source "./sample-files" --apply

Replace `./sample-files` with the path to your own test directory.

## Run tests

    python -m pytest -v

## Project structure

    smart-file-organizer/
    ├── organizer.py
    ├── main.py
    ├── requirements.txt
    ├── README.md
    └── tests/
        └── test_organizer.py

## Limitations

- Organizes files in the selected directory, not recursively.
- File classification is based on extensions, not file contents.
- A failed move does not automatically roll back earlier successful moves.
- Test with sample files before using on important directories.

## Technologies

Python, pathlib, shutil, argparse, dataclasses, pytest
=======
# smart-file-organizer
>>>>>>> fe4f24957b4211dd1901d1a1e39eabd7eb6fa2bf
