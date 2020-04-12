import yaml
import argparse
from munch import DefaultMunch

from genshop.application.app import App


def get_config():
    parser = argparse.ArgumentParser(description='General Shopper')
    parser.add_argument('-config', help='a path to configuration file')

    args = parser.parse_args()
    filename = args.config

    with open(filename, 'r') as file:
        cfg_dict = yaml.load(file)
        return DefaultMunch.fromDict(cfg_dict, None)


def system_start():
    cfg = get_config()
    if cfg is None:
        raise Exception("Unable to extract the given config")

    App(cfg)


if __name__ == "__main__":
    system_start()
