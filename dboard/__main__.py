"""
This module is called when the package is executed as a module.
"""

import importlib
from sys import exit

if __name__ == "__main__":
    try:
        importlib.import_module("dboard.main")
        # from dboard.main import main
    except ImportError as e:
        exit(str(e))
    except KeyboardInterrupt:
        print("\nQuitting...")
        exit()
    finally:
        print("dboard exit.")

    exit()
