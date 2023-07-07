"""
Home to the shadow_copy function
"""

import ctypes
import logging
import os
import shutil
import textwrap
from pathlib import Path
from typing import Union

import wmi

from .exceptions import (
    OSUnsupportedError,
    PathIsNotToFile,
    RequiresAdminError,
    ShadowCopyFailure,
)

logger = logging.getLogger(__name__)


def _is_os_supported() -> bool:
    """Private method for checking if os is supported"""
    return os.name == "nt"


def _is_admin() -> bool:
    """Private method for checking if we're admin"""
    return ctypes.windll.shell32.IsUserAnAdmin() != 0


def shadow_copy(src: Union[str, Path], dst: Union[str, Path]) -> None:
    """
    Copies the src file to the dst path using a shadow copy.

    In order to use this function, you must be running as admin and on Windows.
    Shadow copies are normally used to allow in use files to be copied and backed up.
    """
    if not _is_os_supported():
        raise OSUnsupportedError(f"This OS is not supported: {os.name}")

    if not _is_admin():
        raise RequiresAdminError("This operation requires admin. Please run as admin.")

    if not Path(src).is_file():
        raise PathIsNotToFile(f"The src path is not a file: {src}")

    # Need fully resolved path for shadow copy
    src = Path(src).resolve()
    dst = Path(dst).resolve()

    c = wmi.WMI()
    drive_letter_with_colon, rest_of_path = os.path.splitdrive(src)
    rest_of_path = rest_of_path.lstrip(os.sep)

    result, shadow_id = c.Win32_ShadowCopy.Create(
        Context="ClientAccessible", Volume=f"{drive_letter_with_colon}{os.sep}"
    )

    if result != 0:
        raise ShadowCopyFailure(
            textwrap.dedent(
                f"""
                Unable to create a shadow copy of the source file.
                Win32_ShadowCopy. Create Error: {result}."""
            )
        )

    shadow_obj = c.Win32_ShadowCopy(ID=shadow_id)[0]
    try:
        shadow_volume_path = shadow_obj.DeviceObject
        logger.debug(f"shadow volume path: {shadow_volume_path}")
        # note that os.path.join(..) does not work properly with shadow_volume_path. It would start with \\?\GLOBALROOT...
        shutil.copy(shadow_volume_path + os.sep + rest_of_path, dst)
    finally:
        # Make sure we remove the newly created shadow copy
        shadow_obj.Delete_()
