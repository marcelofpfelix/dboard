'''
rich library
defines the UI
'''

import asyncio
import sys
from datetime import datetime
from rich import box
from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from dboard import __version__

console = Console()


class Header:
    """
    Display header with clock.
    """

    def __str__(self):
        return self.__class__.__name__

    @classmethod
    def __rich__(cls) -> Panel:
        version = __version__

        grid = Table.grid(expand=True)
        grid.add_column(justify='center', ratio=1)
        grid.add_column(justify='right')
        grid.add_row(
            f'[b]dboard[/b] v{version}',
            datetime.now().ctime().replace(':', '[blink]:[/]'),
        )
        return Panel(grid, style='white on blue')


def make_layout(config) -> Layout:
    """
    Define the layout.
    """
    layout = Layout(name='root')
    my_objects = []

    my_objects.append(Layout(name='header', size=3))

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


async def command(layout, item) -> Panel:
    """
    run a subprocess
    """
    table = Table.grid(padding=0)

    # try:
    proc = await asyncio.create_subprocess_shell(
        item['command'],
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    msg = await proc.stdout.read()

    # except Exception as e:
    #    return ''

    """
    err_message = proc.stderr.read().decode()
    if proc.returncode != 0:
        # the process was not successful
        if "No such file" in err_message:
            raise FileNotFoundError('No such file "me"')

    if stderr:
        print(f"Error occurred: {stderr}")
    else:
        print(f"Output: {stdout}")
    """

    table.add_row(
        f"{msg.decode('utf-8').strip() }"
    )

    message_panel = Panel(table,
                          box=box.ROUNDED,
                          padding=(0, 0),
                          title=item['title'],
                          border_style='bright_blue',
                          )
    layout.update(message_panel)


async def async_dash(config):
    """
    start the dashboard
    """
    # rich refresh rate per second
    refresh_rate = 5
    # Live update duration: 3 hours
    live_duration = 10
    task_timeout = 2

    layout = make_layout(config['layout'])

    layout['header'].update(Header())

    with Live(layout, refresh_per_second=refresh_rate, screen=True):

        # 3 hours timeout
        for index in range(refresh_rate * live_duration):

            for item in config['layout']:
                if 'split_row' in item:
                    for item2 in item['split_row']:
                        if index % (item2['refresh'] * refresh_rate) == 0:
                            asyncio.create_task(command(layout[item2['name']], item2))
                else:
                    if index % (item['refresh'] * refresh_rate) == 0:
                        asyncio.create_task(command(layout[item['name']], item))

            await asyncio.sleep(1/refresh_rate)

        # cancel async tasks
        tasks = asyncio.all_tasks()

        # Shield the cleanup process from cancellation
        # await asyncio.gather(*tasks, return_exceptions=True)
        for task in tasks:
            try:
                print('Finishing tasks')
                await asyncio.wait_for(task, timeout=task_timeout)
            except TimeoutError:
                print('The task was cancelled due to a timeout')
            except asyncio.CancelledError:
                print('The tasks have ended.')

    sys.exit()


def start_dash(config) -> int:
    """
    start the dashboard
    """

    try:
        return asyncio.run(async_dash(config))
    except KeyboardInterrupt:
        print('\nQuitting...')
        sys.exit()
