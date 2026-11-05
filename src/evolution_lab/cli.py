"""Minimal research CLI; no data download is performed implicitly."""
import argparse
from .panel import sustained_entry

def main():
    parser = argparse.ArgumentParser(description="Economic Evolution Lab")
    parser.add_argument("--version", action="store_true", help="Print package version")
    args = parser.parse_args()
    if args.version:
        from . import __version__
        print(__version__)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
