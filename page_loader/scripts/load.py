#!/usr/bin/env python

"""Run script module."""

import os

import argparse

from page_loader.dowloader import download


def main():
    """Run script."""
    parser = argparse.ArgumentParser(description='page-loader')
    parser.add_argument('--output', type=str, default=os.getcwd())
    parser.add_argument('url', type=str)
    args = parser.parse_args()
    download(args.output, args.url)


if __name__ == '__main__':
    main()
