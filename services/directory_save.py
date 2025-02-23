import configparser
import os

CONFIG_FILE = "config.ini"


def save_directory(directory):
    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)

    if "Settings" not in config:
        config["Settings"] = {}
    config["Settings"]["selected_directory"] = directory

    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def load_directory():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return config.get("Settings", "selected_directory", fallback=None)
    return None


def output_directory(directory):
    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)

    if "Settings" not in config:
        config["Settings"] = {}
    config["Settings"]["output_directory"] = directory

    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def load_output_directory():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return config.get("Settings", "output_directory", fallback=None)
    return None
