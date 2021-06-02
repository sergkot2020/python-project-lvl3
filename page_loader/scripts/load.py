#!/usr/bin/env python

"""Run script module."""

import sys

import page_loader
import requests
from page_loader.logger import get_logger

logger = get_logger(__name__)


def main():
    url, path = page_loader.parse()
    exit_code = 0
    try:
        page_path = page_loader.download(url, path=path)
        print(page_path)
    except FileNotFoundError:
        exit_code = 1
        logger.error(f'Directory {path} doesn`t exist')
    except requests.exceptions.ConnectionError:
        exit_code = 1
        logger.error('Network problems')
    except requests.exceptions.HTTPError:
        exit_code = 1
        logger.error('Page not found')
    except PermissionError:
        exit_code = 1
        logger.error(
            'No permission to write the file to the directory'
        )
    except Exception as e:
        exit_code = 1
        logger.exception(e)
    finally:
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
