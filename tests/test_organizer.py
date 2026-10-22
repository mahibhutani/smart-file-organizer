
"""Tests for the Smart File Organizer."""

from pathlib import Path

from organizer import FileOrganizer


def test_plan_does_not_move_files(tmp_path: Path) -> None:
    source = tmp_path / "sample"
    source.mkdir()
    file_path = source / "photo.jpg"
    file_path.write_text("sample image data")

    actions = FileOrganizer(source).organize()

    assert len(actions) == 1
    assert actions[0].destination.parent.name == "Images"
    assert file_path.exists()


def test_apply_moves_file(tmp_path: Path) -> None:
    source = tmp_path / "sample"
    source.mkdir()
    file_path = source / "notes.txt"
    file_path.write_text("hello")

    actions = FileOrganizer(source).organize(apply=True)

    assert len(actions) == 1
    assert (source / "Documents" / "notes.txt").read_text() == "hello"
    assert not file_path.exists()


def test_unknown_extension_goes_to_others(tmp_path: Path) -> None:
    source = tmp_path / "sample"
    source.mkdir()
    (source / "data.xyz").write_text("example")

    actions = FileOrganizer(source).plan()

    assert actions[0].destination.parent.name == "Others"


def test_existing_destination_is_not_overwritten(
    tmp_path: Path,
) -> None:
    source = tmp_path / "sample"
    source.mkdir()
    images = source / "Images"
    images.mkdir()

    (source / "photo.jpg").write_text("new content")
    (images / "photo.jpg").write_text("existing content")

    FileOrganizer(source).organize(apply=True)

    assert (images / "photo.jpg").read_text() == "existing content"
    assert (images / "photo_1.jpg").read_text() == "new content"


def test_directories_are_not_processed(tmp_path: Path) -> None:
    source = tmp_path / "sample"
    source.mkdir()
    (source / "subfolder").mkdir()
    (source / "notes.txt").write_text("hello")

    actions = FileOrganizer(source).plan()

    assert len(actions) == 1
    assert actions[0].source.name == "notes.txt"
