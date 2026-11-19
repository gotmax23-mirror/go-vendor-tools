# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

import io
import uuid
from pathlib import Path
from tarfile import DIRTYPE, REGTYPE, TarInfo

from go_vendor_tools.archive import OurTarFile, get_toplevel_directory

TEST_ARCHIVES_FOLDER = "test_source_archives"


def test_get_toplevel_directory_single_top_level_directory(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(
        tmp_path,
        "test-src-1.1.1/",
        "test-src-1.1.1/src.txt",
        "test-src-1.1.1/src.go",
        "test-src-1.1.1/src.java",
    )
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual == "test-src-1.1.1"


def test_get_toplevel_directory_only_files_in_top_level(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(
        tmp_path,
        "test-src-1.1.1/src.txt",
        "test-src-1.1.1/src.go",
        "test-src-1.1.1/src.java",
    )
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual == "test-src-1.1.1"


def test_get_toplevel_directory_multiple_top_level_directories(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(
        tmp_path,
        "additional_dir/",
        "additional_dir/text.txt",
        "additional_dir/text.md",
        "test-src-1.1.1/",
        "test-src-1.1.1/src.txt",
        "test-src-1.1.1/src.go",
        "test-src-1.1.1/src.java",
    )
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual is None


def test_get_toplevel_directory_multi_only_files_at_top_level(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(
        tmp_path,
        "additional_dir/text.txt",
        "additional_dir/text.md",
        "test-src-1.1.1/src.txt",
        "test-src-1.1.1/src.go",
        "test-src-1.1.1/src.java",
    )
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual is None


def test_get_toplevel_directory_file_in_root_directory(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(
        tmp_path,
        "file.txt",
        "test-src-1.1.1/",
        "test-src-1.1.1/src.txt",
        "test-src-1.1.1/src.go",
        "test-src-1.1.1/src.java",
    )
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual is None


def test_get_toplevel_directory_dot_dir_is_top_level_directory(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(tmp_path, "./")
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual is None


def test_get_toplevel_directory_dot_and_top_level_directory(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(
        tmp_path,
        "./",
        "test-src-1.1.1/",
        "test-src-1.1.1/src.txt",
        "test-src-1.1.1/src.go",
        "test-src-1.1.1/src.java",
    )
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual == "test-src-1.1.1"


def test_get_toplevel_directory_dot_and_only_files_in_top_level(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(
        tmp_path,
        "./",
        "test-src-1.1.1/src.txt",
        "test-src-1.1.1/src.go",
        "test-src-1.1.1/src.java",
    )
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual == "test-src-1.1.1"


def test_get_toplevel_directory_only_file_in_archive(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(tmp_path, "test.txt")
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual is None


def test_get_toplevel_directory_only_file_with_dot_dir(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(tmp_path, "./", "test.txt")
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual is None


def test_get_toplevel_directory_only_empty_filename_file(tmp_path: Path) -> None:
    TEST_ARCHIVE = _create_test_archive(tmp_path, "")
    test_file = OurTarFile.open(TEST_ARCHIVE)
    actual = get_toplevel_directory(test_file)
    assert actual is None


def _create_test_archive(tmp_path: Path, *file_names: str) -> Path:
    archive_name = str(uuid.uuid4()) + ".tar.gz"
    tmp_archive_path = tmp_path / archive_name
    with OurTarFile.open(tmp_archive_path, "w:gz") as archive:
        for filename in file_names:
            tar_info = TarInfo(filename)
            if filename.endswith("/"):
                tar_info.type = DIRTYPE
                archive.addfile(tar_info)
            else:
                content = bytes(filename, "utf-8")
                tar_info.type = REGTYPE
                tar_info.size = len(content)
                archive.addfile(tar_info, io.BytesIO(content))
    return tmp_archive_path
