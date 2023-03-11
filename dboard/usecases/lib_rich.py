'''
rich library
defines the UI
'''

import time
import subprocess
from datetime import datetime
from rich import box
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

console = Console()


class Header:
    """
    Display header with clock.
    """

    def __str__(self):
        return self.__class__.__name__

    @classmethod
    def __rich__(cls) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]tdash[/b] v0.1.0",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")


def make_layout(config) -> Layout:
    """
    Define the layout.
    """
    layout = Layout(name="root")
    my_objects = []

    my_objects.append(Layout(name="header", size=3))

    # this should in the future set defaut values or test if key exists
    for item in config:
        my_objects.append(Layout(name=item['name'], size=item['size']))

    layout.split(*my_objects)

    # create split row (create frunction)
    for item in config:
        if 'split_row' in item:
            my_objects2 = []
            for item2 in item['split_row']:
                my_objects2.append(Layout(name=item2['name']))
            layout[item['name']].split_row(*my_objects2)

    return layout


def command(item) -> Panel:
    """
    run a subprocess
    """
    table = Table.grid(padding=0)

    process = subprocess.run(item['command'],
                             capture_output=True, text=True, check=True)
    table.add_row(
        f"{process.stdout}"
    )

    message_panel = Panel(table,
                          box=box.ROUNDED,
                          padding=(0, 0),
                          title=item['title'],
                          border_style="bright_blue",
                          )
    return message_panel


def start_dash(config):
    """
    start the dashboard
    """

    layout = make_layout(config['layout'])

    layout["header"].update(Header())

    for item in config['layout']:
        if 'split_row' in item:
            for item2 in item['split_row']:
                layout[item2['name']].update(command(item2))
        else:
            layout[item['name']].update(command(item))

    with Live(layout, refresh_per_second=1, screen=True):
        for index in range(10800):
            time.sleep(0.8)
            if index % 3 == 0:
                for item in config['layout']:
                    if 'split_row' in item:
                        for item2 in item['split_row']:
                            layout[item2['name']].update(command(item2))
                    else:
                        layout[item['name']].update(command(item))
