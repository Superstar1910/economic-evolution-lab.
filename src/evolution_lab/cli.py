"""Command line entry point for the research pipeline."""
from __future__ import annotations
import argparse
import json
from . import __version__
from .atlas import DEFAULT_COUNTRIES, extract

def main():
    parser = argparse.ArgumentParser(description="Economic Evolution Lab")
    parser.add_argument("--version", action="store_true")
    sub = parser.add_subparsers(dest="command")
    run = sub.add_parser("extract-atlas", help="Fetch a bounded HS92 historical country sample")
    run.add_argument("--countries", nargs="+", default=list(DEFAULT_COUNTRIES))
    run.add_argument("--start", type=int, default=1995)
    run.add_argument("--end", type=int, default=2024)
    run.add_argument("--output", default="data/raw/atlas_hs92_pilot.csv")
    run.add_argument("--delay", type=float, default=0.7, help="Seconds between requests")
    args = parser.parse_args()
    if args.version:
        print(__version__)
    elif args.command == "extract-atlas":
        print(json.dumps(extract(args.output, tuple(c.upper() for c in args.countries),
                                 args.start, args.end, args.delay), indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
