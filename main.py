import tarfile
from typing import Optional
import config
import os

from os import path
from tarfile import TarInfo
from fabric import Connection
from invoke import UnexpectedExit


class ParkunDeploy:
    def __init__(self):
        self.connection = Connection(
            host=config.SERVER,
            user=config.USERNAME,
            port=22,
            connect_kwargs={"password": config.PASSWORD})

    def no_hidden(self, item: TarInfo) -> Optional[TarInfo]:
        relative_path = path.split(item.name)[1]

        for pattern in config.IGNORED:
            if relative_path.startswith(pattern):
                return None

        return item

    def tar(self, folder: str) -> str:
        name = path.basename(folder)

        with tarfile.open(f'{name}.tar.gz', "w:gz") as tar:
            tar.add(folder, arcname=name, filter=self.no_hidden)

        return name

    def rename_previous_version(self, folder_name):
        try:
            self.connection.run(f'mv {folder_name} {folder_name}_old')
        except UnexpectedExit as e:
            print(e.result)

    def deploy(self, folder: str) -> None:
        name = self.tar(folder)
        filename = f'{name}.tar.gz'
        file = path.join(os.getcwd(), filename)
        result = self.connection.put(file, remote='')
        print(f'Uploaded {result.local} to {result.remote}')
        self.connection.run(f'tar xvzf {filename}')

    def stop_previous_bot(self):
        self.safe_run_command(f'cd {config.PARKUN_BOT} && make stop_prod')

        self.connection.run(f'rm -rf {config.PARKUN_BOT}_old')
        self.rename_previous_version(config.PARKUN_BOT)

    def run_bot(self):
        self.connection.run(f'cd {config.PARKUN_BOT} && make start_prod')

    def stop_previous_sender(self):
        self.safe_run_command(f'cd {config.PARKUN_BOT} && make stop')

        self.connection.run(f'rm -rf {config.APPEAL_SENDER}_old')
        self.rename_previous_version(config.APPEAL_SENDER)

    def run_sender(self):
        self.connection.run(f'cd {config.APPEAL_SENDER} && make start')

    def upload_makefile(self):
        filename = 'Makefile'
        file = path.join(os.getcwd(), filename)
        result = self.connection.put(file, remote='')
        print(f'Uploaded {result.local} to {result.remote}')

    def safe_run_command(self, command: str) -> None:
        try:
            self.connection.run(command)
        except UnexpectedExit as e:
            print(e.result)

    def start(self) -> None:
        self.stop_previous_bot()
        self.deploy(config.BOT_FOLDER)
        self.run_bot()

        self.stop_previous_sender()
        self.deploy(config.SENDER_FOLDER)
        self.run_sender()

        self.upload_makefile()


if __name__ == "__main__":
    ParkunDeploy().start()
