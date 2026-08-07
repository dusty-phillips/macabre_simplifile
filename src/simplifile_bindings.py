import errno
import os
import shutil

from gleam_builtins import Error, Nil, Ok, to_gleam_list

# Maps Python errno values to the corresponding FileError variant names defined
# in simplifile.gleam. Constructors are looked up lazily on the compiled
# simplifile module to avoid a circular import at module load time.
_ERRNO_NAMES = [
    ("EACCES", "Eacces"),
    ("EAGAIN", "Eagain"),
    ("EBADF", "Ebadf"),
    ("EBADMSG", "Ebadmsg"),
    ("EBUSY", "Ebusy"),
    ("EDEADLK", "Edeadlk"),
    ("EDEADLOCK", "Edeadlock"),
    ("EDQUOT", "Edquot"),
    ("EEXIST", "Eexist"),
    ("EFAULT", "Efault"),
    ("EFBIG", "Efbig"),
    ("EFTYPE", "Eftype"),
    ("EINTR", "Eintr"),
    ("EINVAL", "Einval"),
    ("EIO", "Eio"),
    ("EISDIR", "Eisdir"),
    ("ELOOP", "Eloop"),
    ("EMFILE", "Emfile"),
    ("EMLINK", "Emlink"),
    ("EMULTIHOP", "Emultihop"),
    ("ENAMETOOLONG", "Enametoolong"),
    ("ENFILE", "Enfile"),
    ("ENOBUFS", "Enobufs"),
    ("ENODEV", "Enodev"),
    ("ENOLCK", "Enolck"),
    ("ENOLINK", "Enolink"),
    ("ENOENT", "Enoent"),
    ("ENOMEM", "Enomem"),
    ("ENOSPC", "Enospc"),
    ("ENOSR", "Enosr"),
    ("ENOSTR", "Enostr"),
    ("ENOSYS", "Enosys"),
    ("ENOTBLK", "Enotblk"),
    ("ENOTDIR", "Enotdir"),
    ("ENOTSUP", "Enotsup"),
    ("ENXIO", "Enxio"),
    ("EOPNOTSUPP", "Eopnotsupp"),
    ("EOVERFLOW", "Eoverflow"),
    ("EPERM", "Eperm"),
    ("EPIPE", "Epipe"),
    ("ERANGE", "Erange"),
    ("EROFS", "Erofs"),
    ("ESPIPE", "Espipe"),
    ("ESRCH", "Esrch"),
    ("ESTALE", "Estale"),
    ("ETXTBSY", "Etxtbsy"),
    ("EXDEV", "Exdev"),
]


def _errno_to_variant():
    mapping = {}
    for attribute, variant in _ERRNO_NAMES:
        code = getattr(errno, attribute, None)
        if code is not None:
            mapping[code] = variant
    return mapping


_ERRNO_TO_VARIANT = _errno_to_variant()


def _cast_error(exc):
    import simplifile as simplifile_module

    name = _ERRNO_TO_VARIANT.get(getattr(exc, "errno", None))
    if name is None:
        return simplifile_module.Unknown(str(exc))
    constructor = getattr(simplifile_module, name, None)
    if constructor is None:
        return simplifile_module.Unknown(str(exc))
    return constructor()


def _guard(op):
    try:
        return Ok(op())
    except Exception as exc:
        return Error(_cast_error(exc))


def file_info(filepath):
    def op():
        import simplifile as simplifile_module

        stat = os.stat(filepath)
        return simplifile_module.FileInfo(
            size=stat.st_size,
            mode=stat.st_mode,
            nlinks=stat.st_nlink,
            inode=stat.st_ino,
            user_id=stat.st_uid,
            group_id=stat.st_gid,
            dev=stat.st_dev,
            atime_seconds=int(stat.st_atime),
            mtime_seconds=int(stat.st_mtime),
            ctime_seconds=int(stat.st_ctime),
        )

    return _guard(op)


def link_info(filepath):
    def op():
        import simplifile as simplifile_module

        stat = os.lstat(filepath)
        return simplifile_module.FileInfo(
            size=stat.st_size,
            mode=stat.st_mode,
            nlinks=stat.st_nlink,
            inode=stat.st_ino,
            user_id=stat.st_uid,
            group_id=stat.st_gid,
            dev=stat.st_dev,
            atime_seconds=int(stat.st_atime),
            mtime_seconds=int(stat.st_mtime),
            ctime_seconds=int(stat.st_ctime),
        )

    return _guard(op)


def read_bits(filepath):
    def op():
        with open(filepath, "rb") as file:
            return file.read()

    return _guard(op)


def write_bits(filepath, bits):
    def op():
        with open(filepath, "wb") as file:
            file.write(bits)
        return Nil

    return _guard(op)


def append_bits(filepath, bits):
    def op():
        with open(filepath, "ab") as file:
            file.write(bits)
        return Nil

    return _guard(op)


def delete(file_or_dir_path):
    def op():
        if os.path.isdir(file_or_dir_path) and not os.path.islink(
            file_or_dir_path
        ):
            shutil.rmtree(file_or_dir_path)
        else:
            os.unlink(file_or_dir_path)
        return Nil

    return _guard(op)


def delete_file(file_path):
    def op():
        os.unlink(file_path)
        return Nil

    return _guard(op)


def read_directory(filepath):
    def op():
        return to_gleam_list(os.listdir(filepath))

    return _guard(op)


def create_directory(filepath):
    def op():
        os.mkdir(filepath)
        return Nil

    return _guard(op)


def create_symlink(target, symlink):
    def op():
        os.symlink(target, symlink)
        return Nil

    return _guard(op)


def create_link(target, link):
    def op():
        os.link(target, link)
        return Nil

    return _guard(op)


def create_dir_all(dirpath):
    def op():
        os.makedirs(dirpath, exist_ok=True)
        return Nil

    return _guard(op)


def copy_file(src, dest):
    def op():
        shutil.copyfile(src, dest)
        return 0

    return _guard(op)


def rename_file(src, dest):
    def op():
        os.rename(src, dest)
        return Nil

    return _guard(op)


def set_permissions_octal(filepath, permissions):
    def op():
        os.chmod(filepath, permissions)
        return Nil

    return _guard(op)


def current_directory():
    def op():
        return os.getcwd()

    return _guard(op)


def resolve(filepath):
    return os.path.abspath(filepath)


def touch(filepath):
    def op():
        try:
            os.utime(filepath, None)
        except FileNotFoundError:
            with open(filepath, "wb"):
                pass
        return Nil

    return _guard(op)
