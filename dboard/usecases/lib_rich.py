"""
rich library
defines the UI
"""

import asyncio
from datetime import datetime

from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from dboard import __version__
from dboard.usecases.config import Settings, Subprocess

console = Console()


def update_header(config: Settings) -> Panel:
    """
    Update the header
    """
    version = __version__

    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="center", ratio=1)
    grid.add_column(justify="right")
    grid.add_row(
        f"[b]dboard[/b] v{version}",
        f"[b]{config.title}[/b]",
        datetime.now().ctime().replace(":", "[blink]:[/]"),
    )
    return Panel(grid, style=config.header_style)


def make_layout(config: Settings) -> Layout:
    """
    Define the layout.
    """
    layout = Layout(name="root")
    layout_list = []

    layout_list.append(Layout(name="header", size=3))

    # this should in the future set defaut values or test if key exists
    for row in config.layout:
        layout_list.append(Layout(name=row.id, size=row.size))

    layout.split(*layout_list)

    # create split row (create frunction)
    for row in config.layout:
        subprocess_list = []
        for subprocess in row.subprocess:
            subprocess_list.append(Layout(name=subprocess.id))
        layout[str(row.id)].split_row(*subprocess_list)

    return layout


async def command(layout: Layout, subprocess: Subprocess) -> None:
    """
    run a subprocess
    """
    table = Table.grid(padding=0)

    # try:
    proc = await asyncio.create_subprocess_shell(
        subprocess.command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if stdout:
        table.add_row(f"{stdout.decode('utf-8').strip()}")
    if stderr:
        table.add_row(
            f"{stderr.decode('utf-8').strip()}, exited with {proc.returncode}"
        )
        # if "No such file" in err_message:
        #     raise FileNotFoundError('No such file')

    message_panel = Panel(
        table,
        box=box.ROUNDED,
        padding=(0, 0),
        title=subprocess.title,
        border_style=subprocess.border_style,
    )
    layout.update(message_panel)


async def async_dash(config: Settings) -> int:
    """
    start the dashboard
    """
    # rich refresh rate per second
    refresh_rate = 1 / config.rate
    # Live update duration: 3 hours
    live_duration = config.live_duration
    task_timeout = config.task_timeout

    layout = make_layout(config)

    header_panel = update_header(config)
    layout["header"].update(header_panel)
    # layout["header"].update(Header())

    with Live(layout, refresh_per_second=refresh_rate, screen=True):
        # 3 hours timeout
        for index in range(int(live_duration * refresh_rate)):
            for row in config.layout:
                for subprocess in row.subprocess:
                    if index % (subprocess.refresh * refresh_rate) == 0:
                        asyncio.create_task(
                            command(layout[str(subprocess.id)], subprocess)
                        )

            await asyncio.sleep(1 / refresh_rate)

        # cancel async tasks
        tasks = asyncio.all_tasks()

        # Shield the cleanup process from cancellation
        # await asyncio.gather(*tasks, return_exceptions=True)
        for task in tasks:
            try:
                print("Finishing tasks")
                await asyncio.wait_for(task, timeout=task_timeout)
            except TimeoutError:
                print("The task was cancelled due to a timeout")
            except asyncio.CancelledError:
                print("The tasks have ended.")

    return 0
    # sys.exit()


def start_dash(config: Settings) -> int:
    """
    start the dashboard
    """

    try:
        return asyncio.run(async_dash(config))
    except KeyboardInterrupt:
        print("\nQuitting...")
        return 0
