from hashlib import md5
from app_variacao.soup_files import (
    File, Directory, ContentFiles, EnumDocFiles, UserAppDir, UserFileSystem
)


def get_md5_bytes(data: bytes) -> str:
    return md5(data).hexdigest().upper()
