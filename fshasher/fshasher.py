"""
The fshasher provides basic and utilitarian functionality to hash file system objects.
It is cross-platform, intuitive, and simple.
"""

import hashlib
import os
import operator
from pathlib import Path
from typing import Final, Iterable, Protocol


def fshash(path: Path) -> str:
    """
    Hashes the file object based on its contents.

    Args:
        path: The location to hash. Can be a file or a directory.

    Returns:
        The hash of the file object at the path as a string in hex format.
    """
    __blocksize: Final[int] = 4096

    hash_obj = hashlib.sha256()

    if path.is_file():
        # This ensures that for a single file, the hash is the same as that for the content.
        # This guarantee isn't required for a directory since there is no natural hashing
        # value for a directory, and we do not include the filename.
        _add_file_contents_to_hash(hash_obj, curpath, __blocksize)
    else:
        paths = [path]
        while paths:
            curpath = paths.pop()

            # Normalize the separators to '/'. This assumes the only other separator for
            # platforms that run python are '\' (notably Windows), and that all separators
            # unambiguous. For example, Windows does not allow '/' in file names even though
            # it does not have additional meaning.
            relative_path_name = str(curpath.relative_to(path))
            if os.sep == '\\':
                fs_neutral_name = relative_path_name.replace(os.sep, '/')
            else:
                fs_neutral_name = relative_path_name

            if curpath.is_dir():
                hash_obj.update(fs_neutral_name)

                fs_iter = _cross_platform_stable_fs_iter(curpath)
                for child in fs_iter:
                    paths.append(child)
            else:
                hash_obj.update(fs_neutral_name)
                _add_file_contents_to_hash(hash_obj, curpath, __blocksize)

    return hash_obj.hexdigest()


class _Hasher(Protocol):
    """
    Defines the Hasher protocol which is required for all underlying hash implementations.
    """
    def update(b: bytes) -> None:
        """
        Updates the underlying state with the bytes object.

        Args:
            b: The bytes to update the hash with.
        """
        pass

    def hexdigest() -> str:
        """
        Creates a hex formatted digest using the existing data.

        Returns:
            A string of the current hashed data in hex format.
        """
        pass


def _cross_platform_stable_fs_iter(dir: Path) -> Iterable[Path]:
    """
    Provides a stable ordering across platforms over a directory Path.

    This allows iteration across filesystems in a consistent way such that case
    sensitivity of the underlying system does not affect how the files are
    iterated.

    Args:
        dir: The Path object that points to the directory to iterate over.

    Returns:
        An iterator that goes over the paths in the directory, defined in such a
        way that is consistent across platforms.
    """
    tupled = map(lambda p: (str(p), p), dir.iterdir())
    sorted_paths = sorted(tupled, key=operator.itemgetter(0))
    only_paths = map(operator.itemgetter(1), sorted_paths)

    return only_paths


def _add_file_contents_to_hash(hash_obj: _Hasher, path: Path, block_size: int) -> None:
    """
    Helper method in calculating a path's hash to add the hash of a file.

    Args:
        hash_obj: The object that is able to hash the file contents.
        path: The location of the file.
        block_size: The size of the blocks to read in.
    """
    with open(path, 'rb') as f:
        buffer = f.read(block_size)
        while buffer:
            hash_obj.update(buffer)
            buffer = f.read(block_size)
