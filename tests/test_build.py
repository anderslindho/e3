from pathlib import Path

from e3.build.build import create_local_files

RELEASE_LOCAL_CONTENT = """
EPICS_BASE:=/epics/base-7.0.5
E3_REQUIRE_VERSION:=3.4.1
"""


def test_create_local_file_creates_file(tmp_path):
    tmp_dir = tmp_path / "sub"
    tmp_dir.mkdir()
    create_local_files(tmp_dir, Path("/epics"), "7.0.5", "3.4.1")
    local_file = tmp_dir / "RELEASE.local"
    assert local_file.read_text() == RELEASE_LOCAL_CONTENT
    assert len(list(tmp_path.iterdir())) == 1
