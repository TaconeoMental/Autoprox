#!/usr/bin/env python3

import argparse

from src.logger import LOGGER
from src.proxy import Proxy

# https://stackoverflow.com/questions/10085996/shutdown-socketserver-serve-forever-in-one-thread-python-application/22533929#22533929

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("source", help="Autoprox config file path.")
    group_verbose = argparser.add_mutually_exclusive_group()
    group_verbose.add_argument("-v", action="count", default=0, help="Verbose count.")
    group_verbose.add_argument("-q", "--quiet", action="store_true", help="Quiet output. Just display necessary information.")
    parsed_args = argparser.parse_args()

    verbose_level = 0
    if parsed_args.quiet:
        LOGGER.quiet()
    else:
        LOGGER.set_level(parsed_args.v)

    main_proxy = Proxy()
    main_proxy.set_config_file(parsed_args.source)
    main_proxy.run()


if __name__ == '__main__':
    main()
