from pushbullet import Pushbullet
from lib import Functions as f


class PushBullet:
    def __init__(self, config_all):
        self.config = config_all

    def Send(self, text):
        pb = Pushbullet(self.config["Pushbullet"]["apikey"])
        pb.push_note(f.Goede(self.config), f.html2plain(text))
