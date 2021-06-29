from yaml import load
from yaml import CLoader as Loader
import os


class Config:

    @staticmethod
    def get(key):
        config = load(open(os.path.join(os.path.dirname(__file__), '../config.yml'), "r"), Loader=Loader)
        return config[key]
