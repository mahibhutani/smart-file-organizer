
"""Core functionality for the Smart File Organizer."""

from dataclasses import dataclass
from pathlib import Path
import shutil


FILE_CATEGORIES = {
    "Images": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".xlsx", ".csv", ".pptx"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi"},
    "Audio": {".mp3", ".wav", ".aac", ".flac"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".cpp"},
}


@dataclass(frozen=True)
class FileAction:
    """Describe a planned file move."""

    source: Path
    destination: Path


class FileOrganizer:
    """Organize files in one directory by extension."""

    def __init__(self, source_dir: str | Path) -> None:
        self.source_dir = Path(source_dir).expanduser().resolve()

        if not self.source_dir.is_dir():
            raise NotADirectoryError(
                f"Source directory does not exist: {self.source_dir}"
            )

    @staticmethod
    def _category_for(file_path: Path) -> str:
        """Return the category matching a file extension."""
        extension = file_path.suffix.lower()

        for category, extensions in FILE_CATEGORIES.items():
            if extension in extensions:
                return category

        return "Others"

    @staticmethod
    def _unique_path(path: Path) -> Path:
        """Choose a non-existing path without overwriting a file."""
        if not path.exists():
            return path

        counter = 1
        while True:
            candidate = path.with_name(
                f"{path.stem}_{counter}{path.suffix}"
            )
            if not candidate.exists():
                return candidate
            counter += 1

    def plan(self) -> list[FileAction]:
        """Preview moves without changing any files."""
        actions = []

        for file_path in sorted(self.source_dir.iterdir()):
            # Do not follow symbolic links or process directories.
            if file_path.is_symlink() or not file_path.is_file():
                continue

            category = self._category_for(file_path)
            target_dir = self.source_dir / category
            destination = self._unique_path(target_dir / file_path.name)

            actions.append(
                FileAction(source=file_path, destination=destination)
            )

        return actions

    def organize(self, apply: bool = False) -> list[FileAction]:
        """
        Return planned actions; move files only when apply=True.

        Existing destination files are never intentionally overwritten.
        """
        actions = self.plan()

        if not apply:
            return actions

        completed = []

        for action in actions:
            try:
                action.destination.parent.mkdir(
                    parents=True, exist_ok=True
                )

                # Recheck immediately before moving to reduce collision risk.
                destination = self._unique_path(action.destination)

                shutil.move(
                    str(action.source),
                    str(destination),
                )

                completed.append(
                    FileAction(action.source, destination)
                )
            except OSError as error:
                print(f"Could not move {action.source.name}: {error}")

        return completed
