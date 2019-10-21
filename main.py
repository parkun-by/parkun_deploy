import fabric
import tarfile
import config

from os import path
from tarfile import TarInfo


def no_hidden(item: TarInfo) -> TarInfo or None:
    relative_path = path.split(item.name)[1]

    for pattern in config.IGNORED:
        if relative_path.startswith(pattern):
            return None

    return item


def tar(folder: str):
    name = path.basename(folder)

    with tarfile.open(f'{name}.tar.gz', "w:gz") as tar:
        tar.add(folder, arcname=name, filter=no_hidden)


def deploy(folder: str) -> None:
    tar(folder)


def start() -> None:
    deploy(config.BOT_FOLDER)
    deploy(config.PREPARER_FOLDER)


if __name__ == "__main__":
    start()
