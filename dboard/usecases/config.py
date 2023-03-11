"""
config.py
manages the config template file
"""

import yaml

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
        print("Error: File does not appear to exist.")

        with open(config_path, 'w', encoding="utf-8") as file:
            yaml.dump(example, file)

    return example
