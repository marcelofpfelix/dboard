"""
config.py
manages the config template file
"""

from pathlib import Path
import yaml

example = {'layout': [{'name': 'ipping', 'size': 10, 'split_row':
                       [{'command': 'ip -br -4 a', 'name': 'ip',
                         'refresh': 30, 'title': '\U0001F9A9  ip addr'},
                        {'command': 'ping -c 1 1.1.1.1', 'name': 'ping',
                         'refresh': 0.6, 'title': '\U0001F980  ping'}]},
                      {'command': 'vmstat', 'name': 'vmstat', 'refresh': 1,
                       'size': 5, 'title': '\U0001F422  vmstat'},
                      {'command': 'uptime', 'name': 'uptime',
                       'refresh': 2, 'size': 3, 'title': '\U0001F408  uptime'}]}


def get_config(config_path):
    """
    read the config template file
    writes the default template if it doesn't exist

    arg config_path: config file path
    return: a dict with the configuration
    """
    try:
        with open(config_path, encoding="utf-8") as file:
            try:
                config = yaml.safe_load(file)
                return config
            except yaml.YAMLError as exception:
                print(exception)
    except IOError:
        home = str(Path.home()) + "/.dboard/"
        Path(home).mkdir(parents=True, exist_ok=True)
        home += "config.yml"

        print(f"Warning: using default config in {home}")
        with open(home, 'w', encoding="utf-8") as file:
            yaml.dump(example, file)

    return example
