import os
from os import path

SERVER = 'host'
USERNAME = 'username'
PASSWORD = 'password'

PARKUN_BOT = 'parkun-bot'
APPEAL_PREPARER = 'appeal_preparer'

BOT_FOLDER = path.join(os.sep, 'home', 'skaborik', 'Repos', PARKUN_BOT)

PREPARER_FOLDER = path.join(
    os.sep, 'home', 'skaborik', 'Repos', APPEAL_PREPARER)

IGNORED = [
    f'.',
    f'__pycache__',
    f'.Python',
    f'build{os.sep}',
    f'develop-eggs{os.sep}',
    f'dist{os.sep}',
    f'downloads{os.sep}',
    f'eggs{os.sep}',
    f'.eggs{os.sep}',
    f'lib{os.sep}',
    f'lib64{os.sep}',
    f'parts{os.sep}',
    f'sdist{os.sep}',
    f'var{os.sep}',
    f'wheels{os.sep}',
    f'pip-wheel-metadata{os.sep}',
    f'shar{os.sep}python-wheels{os.sep}',
    f'.installed.cfg',
    f'MANIFEST',
    f'pip-log.txt',
    f'pip-delete-this-directory.txt',
    f'htmlcov{os.sep}',
    f'.tox{os.sep}',
    f'.nox{os.sep}',
    f'.coverage',
    f'.cache',
    f'nosetests.xml',
    f'coverage.xml',
    f'.hypothesis{os.sep}',
    f'.pytest_cache{os.sep}',
    f'local_settings.py',
    f'db.sqlite3',
    f'db.sqlite3-journal',
    f'instance{os.sep}',
    f'.webassets-cache',
    f'.scrapy',
    f'doc{os.sep}_build{os.sep}',
    f'target{os.sep}',
    f'.ipynb_checkpoints',
    f'profile_default{os.sep}',
    f'ipython_config.py',
    f'.python-version',
    f'celerybeat-schedule',
    f'.env',
    f'.venv',
    f'env{os.sep}',
    f'venv{os.sep}',
    f'ENV{os.sep}',
    f'env.bak{os.sep}',
    f'venv.bak{os.sep}',
    f'.spyderproject',
    f'.spyproject',
    f'.ropeproject',
    f'.mypy_cache{os.sep}',
    f'.dmypy.json',
    f'dmypy.json',
    f'.pyre{os.sep}',
]
