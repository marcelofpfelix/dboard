"""
config.py
manages the config template file
"""

from pathlib import Path
from sys import exit
from typing import Any, List
from uuid import uuid4

import yaml
from pydantic import BaseModel, Field, ValidationError

example = {
    "title": "My Dashboard",
    "header_style": "white on blue",
    "live_duration": 10800,
    "layout": [
        {
            "size": 10,
            "subprocess": [
                {"command": "ss -s", "refresh": 2, "title": "🦩  ss"},
                {
                    "command": "ping -c 1 1.1",
                    "refresh": 0.2,
                    "title": "🦀  ping",
                    "border_style": "bright_blue",
                },
            ],
        },
        {"size": 5, "subprocess": [{"command": "vmstat -S M", "title": "🐢  vmstat"}]},
        {"size": 3, "subprocess": [{"command": "uptime", "title": "🐈  uptime"}]},
        {"size": 3, "subprocess": [{"command": "notfound", "title": "🐈  notfound"}]},
    ],
}


def read_yaml(config_path: str) -> Any:
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


class Subprocess(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    command: str
    refresh: float = Field(ge=0.2, multiple_of=0.1, default=1)
    title: str = Field(max_length=60)
    border_style: str = Field(default="bright_blue")
    # extra validation todo:
    # refresh should be a multiple of rate


class Layout(BaseModel):
    id: str | None = Field(default_factory=lambda: uuid4().hex)
    size: int = Field(gt=0)
    subprocess: List[Subprocess]


class Settings(BaseModel):
    rate: float = Field(ge=0.1, multiple_of=0.1, default=0.1)
    title: str = Field(default="", max_length=60)
    live_duration: int = Field(gt=0, default=10800)
    task_timeout: int = Field(gt=0, default=2)
    header_style: str = Field(default="white on blue")
    layout: List[Layout]


def get_config(config_path: str) -> Settings:
    """
    Converts the json config to a pydantic
    data validation model
    """

    json_config = read_yaml(config_path)

    try:
        config = Settings(**json_config)
    except ValidationError as e:
        print(e.errors())
        exit()

    return config
