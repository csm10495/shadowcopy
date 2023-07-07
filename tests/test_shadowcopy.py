"""
Home to tests for shadowcopy
"""

from unittest.mock import patch

import pytest

from shadowcopy.exceptions import (
    OSUnsupportedError,
    PathIsNotToFile,
    RequiresAdminError,
)
from shadowcopy.shadow import _is_admin, shadow_copy


@pytest.fixture(scope="function")
def admin_required():
    if not _is_admin():
        pytest.skip("Skipping because this test requires admin")


def test_shadow_copy_full(tmp_path, admin_required):
    src = tmp_path / "src.txt"
    src.write_text("hello world")

    dst = tmp_path / "dst.txt"
    dst.write_text("goodbye world")

    assert shadow_copy(src, dst) is None

    assert dst.read_text() == "hello world"
    assert src.read_text() == "hello world"


def test_shadow_copy_raises_osunsupported():
    with patch("shadowcopy.shadow._is_os_supported", return_value=False):
        with patch("shadowcopy.shadow.os.name", "lol"):
            with pytest.raises(OSUnsupportedError) as ex:
                shadow_copy("src.txt", "dst.txt")

    assert str(ex.value) == "This OS is not supported: lol"


def test_shadow_copy_raises_requiresadmin():
    with patch("shadowcopy.shadow._is_os_supported", return_value=True):
        with patch("shadowcopy.shadow._is_admin", return_value=False):
            with pytest.raises(RequiresAdminError) as ex:
                shadow_copy("src.txt", "dst.txt")

        assert str(ex.value) == "This operation requires admin. Please run as admin."


def test_shadow_copy_raises_pathisnottofile(tmp_path):
    with patch("shadowcopy.shadow._is_os_supported", return_value=True):
        with patch("shadowcopy.shadow._is_admin", return_value=True):
            with pytest.raises(PathIsNotToFile) as ex:
                shadow_copy(tmp_path, "dst.txt")

    assert str(ex.value) == f"The src path is not a file: {tmp_path}"
