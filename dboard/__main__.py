"""
This module is called when the package is executed as a module.
"""

import sys


if __name__ == "__main__":
    try:
        from dboard.main import main
    except ImportError as e:
        sys.exit(e)
    except KeyboardInterrupt:
        print("\nQuitting...")
        sys.exit()
    finally:
        print("dboard exit.")

    sys.exit(main())  # pylint: disable=no-value-for-parameter
