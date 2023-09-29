from . import pages
from ._builtin import Bot


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Welcome, {
            'browser_name': 'test',
            'browser_version': 'test',
            'device': 'test',
            'os_name': 'test',
            'os_version': 'test',
            'fps': 30
            }
