import config
import os

from os import path
from fabric import Connection
from invoke import UnexpectedExit
from dotenv import load_dotenv

load_dotenv()

HOME_FOLDER = os.getenv('HOME_FOLDER')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')


class ParkunDeploy:
    def __init__(self):
        self.connection = Connection(
            host=config.SERVER,
            user=config.USERNAME,
            port=22,
            connect_kwargs={"password": config.PASSWORD})

    def run_parkun(self):
        self.safe_run_command(
            f'export HOME_FOLDER={HOME_FOLDER} &&' +
            f'export REDIS_PASSWORD=\'{REDIS_PASSWORD}\' && ' +
            'make start')

    def stop_current(self):
        self.safe_run_command(
            f'export HOME_FOLDER={HOME_FOLDER} && ' +
            f'export REDIS_PASSWORD=\'{REDIS_PASSWORD}\' && ' +
            'make stop')

    def upload_makefile(self):
        filename = 'Makefile'
        file = path.join(os.getcwd(), filename)
        result = self.connection.put(file, remote=f'{HOME_FOLDER}')
        print(f'Uploaded {result.local} to {result.remote}')

    def upload_docker_compose(self):
        filename = 'docker-compose.yml'
        file = path.join(os.getcwd(), filename)
        result = self.connection.put(file, remote=f'{HOME_FOLDER}/deploy')
        print(f'Uploaded {result.local} to {result.remote}')

        filename = '.env'
        file = path.join(os.getcwd(), filename)
        result = self.connection.put(file, remote=f'{HOME_FOLDER}/deploy')
        print(f'Uploaded {result.local} to {result.remote}')

    def safe_run_command(self, command: str) -> None:
        try:
            self.connection.run(command)
        except UnexpectedExit as e:
            print(e.result)

    def deploy(self):
        self.create_deploy_folder()
        self.create_logs_folder()
        self.upload_configs()
        self.upload_makefile()
        self.upload_docker_compose()

    def upload_configs(self):
        self.upload_parkun_bot_config()
        self.upload_appeal_sender_config()
        self.upload_broadcaster_config()
        self.upload_rabbit_config()
        self.upload_redis_config()

    def upload_redis_config(self):
        self.safe_run_command('mkdir -p deploy/redis')
        directory = path.join(os.getcwd(), 'redis')

        for filename in os.listdir(directory):
            file = os.path.join(directory, filename)

            result = self.connection.put(
                file,
                remote=f'{HOME_FOLDER}/deploy/redis')

            print(f'Uploaded {result.local} to {result.remote}')

    def upload_rabbit_config(self):
        self.safe_run_command('mkdir -p deploy/rabbit')
        directory = path.join(os.getcwd(), 'rabbitmq')

        for filename in os.listdir(directory):
            file = os.path.join(directory, filename)

            result = self.connection.put(
                file,
                remote=f'{HOME_FOLDER}/deploy/rabbit')

            print(f'Uploaded {result.local} to {result.remote}')

    def upload_parkun_bot_config(self):
        self.safe_run_command('mkdir -p deploy/parkun_bot')
        filename = 'config.py'
        file = path.join(os.getcwd(), 'parkun_bot', filename)

        result = self.connection.put(file,
                                     remote=f'{HOME_FOLDER}/deploy/parkun_bot')

        print(f'Uploaded {result.local} to {result.remote}')

    def upload_appeal_sender_config(self):
        self.safe_run_command('mkdir -p deploy/appeal_sender')
        filename = 'config.py'
        file = path.join(os.getcwd(), 'appeal_sender', filename)

        result = self.connection.put(
            file,
            remote=f'{HOME_FOLDER}/deploy/appeal_sender')

        print(f'Uploaded {result.local} to {result.remote}')

    def upload_broadcaster_config(self):
        self.safe_run_command('mkdir -p deploy/broadcaster')
        filename = 'config.py'
        file = path.join(os.getcwd(), 'broadcaster', filename)

        result = self.connection.put(
            file,
            remote=f'{HOME_FOLDER}/deploy/broadcaster')

        print(f'Uploaded {result.local} to {result.remote}')

    def create_deploy_folder(self):
        self.safe_run_command('mkdir -p deploy')

    def create_logs_folder(self):
        self.safe_run_command('mkdir -p logs')

    def start(self) -> None:
        self.stop_current()
        self.deploy()
        self.run_parkun()


if __name__ == "__main__":
    ParkunDeploy().start()
