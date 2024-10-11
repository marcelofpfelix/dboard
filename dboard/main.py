"""
dboard

A terminal dashboard
"""

import argparse
import os

from dboard import usecases


def main() -> None:
    """
    main function
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-c",
        "--config",
        default="~/.config/dboard/config.yml",
        help="Configuration file",
    )

    parser.add_argument(
        "--level", default=os.environ.get("LOG_LEVEL", "INFO"), help="Logging level."
    )
    args = parser.parse_args()

    config = usecases.get_config(args.config)
    usecases.start_dash(config)


main()
