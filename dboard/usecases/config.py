"""
config.py
manages the config template file
"""

from pathlib import Path
import yaml

example = {
    "layout": [
        {
            "name": "ss_ping",
            "size": 10,
            "split_row": [
                {
                    "command": "ss -s",
                    "name": "ss",
                    "refresh": 30,
                    "title": "\U0001F9A9  ss",
                },
                {
                    "command": "ping -c 1 1.1",
                    "name": "ping",
                    "refresh": 0.6,
                    "title": "\U0001F980  ping",
                },
            ],
        },
        {
            "command": "vmstat -S M",
            "name": "vmstat",
            "refresh": 1,
            "size": 5,
            "title": "\U0001F422  vmstat",
        },
        {
            "command": "uptime",
            "name": "uptime",
            "refresh": 2,
            "size": 3,
            "title": "\U0001F408  uptime",
        },
    ]
}


def get_config(config_path):
    """
    read the config template file
    writes the default template if it doesn't exist

    arg config_path: config file path
    return: a dict with the configuration
    """

    config_path = config_path.replace("~", str(Path.home()))

    try:
        with open(config_path, encoding="utf-8") as file:
            try:
                config = yaml.safe_load(file)
                return config
            except yaml.YAMLError as exception:
                print(exception)
    except IOError:
        # create default folders
        Path(config_path.replace("/config.yml", "")).mkdir(parents=True, exist_ok=True)

        print(f"Warning: using default config in {config_path}")
        with open(config_path, "w", encoding="utf-8") as file:
            yaml.dump(example, file)

    return example
