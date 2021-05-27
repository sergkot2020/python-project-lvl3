"""Parser arguments command line"""

import argparse
import os
from typing import Tuple


def parse() -> Tuple[str, str]:
    """Run script."""
    parser = argparse.ArgumentParser(description='page-loader')
    parser.add_argument('--output', type=str, default=os.getcwd())
    parser.add_argument('url', type=str)
    args = parser.parse_args()
    return args.url, args.output
