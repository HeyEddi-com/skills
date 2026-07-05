"""Filesystem helpers for eval sandboxes."""
from __future__ import annotations

import errno
import os
import shutil
import stat
import time
from collections.abc import Callable
from pathlib import Path

# Errnos that often clear after chmod or a short retry (concurrent writers, read-only trees).
_RETRYABLE_RM_ERRNOS = frozenset({
    errno.ENOTEMPTY,  # e.g. Vite writing .vite/ during rmtree
    errno.EBUSY,
    errno.EPERM,
    errno.EACCES,
})


def _chmod_writable(func: Callable[[str], object], path: str, exc: BaseException) -> None:
    if isinstance(exc, PermissionError) or (
        isinstance(exc, OSError) and exc.errno in (errno.EACCES, errno.EPERM, errno.EROFS)
    ):
        os.chmod(path, stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH)
        func(path)
        return
    raise exc


def robust_rmtree(path: Path | str, *, retries: int = 3, retry_delay: float = 0.5) -> None:
    """Remove a directory tree, retrying on transient ENOTEMPTY / permission errors."""
    target = Path(path)
    if not target.exists():
        return

    last_err: OSError | None = None
    for attempt in range(retries):
        try:
            shutil.rmtree(target, onexc=_chmod_writable)
            return
        except OSError as exc:
            last_err = exc
            if exc.errno not in _RETRYABLE_RM_ERRNOS or attempt + 1 >= retries:
                raise
            time.sleep(retry_delay * (attempt + 1))

    if last_err is not None:
        raise last_err
