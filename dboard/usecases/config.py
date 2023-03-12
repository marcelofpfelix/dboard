"""
config.py
manages the config template file
"""

import yaml
from pathlib import Path

example = {'layout': [{'name': 'ipup', 'size': 10, 'split_row':
                       [{'command': ['ip', '-br', '-4', 'a'], 'name': 'ip',
                         'refresh': 5, 'title': '\U0001F4DE ip addr'},
                        {'command': ['uptime', '-p'], 'name': 'uptime',
                         'refresh': 5, 'title': '\U0001F4DE uptime'}]},
                      {'command': ['vmstat'], 'name': 'vmstat', 'refresh': 1,
                       'size': 5, 'title': '\U0001F4EA vmstat'},
                      {'command': ['lsblk', '-e7'], 'name': 'docker',
                       'refresh': 5, 'size': 8, 'title': '\U0001F40B lsblk'}]}


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
