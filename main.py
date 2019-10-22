import fabric
import tarfile
import config
import os
import time

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

    def no_hidden(self, item: TarInfo) -> TarInfo or None:
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
        self.connection.run(f'cd {config.PARKUN_BOT} && make stop_extra_env')
        self.connection.run(f'rm -rf {config.PARKUN_BOT}_old')
        self.rename_previous_version(config.PARKUN_BOT)

    def run_bot(self):
        self.connection.run(f'cd {config.PARKUN_BOT} && make extra_env')
        time.sleep(5)
        self.connection.run(f'cd {config.PARKUN_BOT} && \
                              docker restart parkun_bot')

    def stop_previous_preparer(self):
        try:
            self.connection.run(f'cd {config.APPEAL_PREPARER} && \
                                  kill -9 `cat save_pid.txt`')
        except UnexpectedExit as e:
            print(e.result)

        self.connection.run(f'rm -rf {config.APPEAL_PREPARER}_old')
        self.rename_previous_version(config.APPEAL_PREPARER)

    def run_preparer(self):
        self.connection.run(f'cd {config.APPEAL_PREPARER} && \
                              python3 -m venv .venv && \
                              source .venv/bin/activate && \
                              pip install --upgrade pip && \
                              pip install -r requirements.txt')

        self.connection.run(f'cd {config.APPEAL_PREPARER} && \
                              source .venv/bin/activate && \
                              nohup python main.py > \
                              my.log 2>log.log &')
        print('stop')

    def start(self) -> None:
        self.stop_previous_bot()
        self.deploy(config.BOT_FOLDER)
        self.run_bot()

        self.stop_previous_preparer()
        self.deploy(config.PREPARER_FOLDER)
        self.run_preparer()


if __name__ == "__main__":
    ParkunDeploy().start()
