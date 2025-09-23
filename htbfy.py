#!/usr/bin/env python3

import os

from argparser import create_parser
from htbclient import HTBClient

from dotenv import load_dotenv


def main() -> None:
    # load the HTB app token
    if not load_dotenv():
        log.failure("Couldn't load the app token from the .env file.")
        exit(-1)
    elif not os.getenv("HTB_APP_TOKEN"):
        log.failure("Couldn't load the app token from the environment.")
        exit(-1)
    else:
        app_token = os.getenv("HTB_APP_TOKEN")

    # instantiate the HTBClient class
    htb_client = HTBClient(app_token)

    # create the parser and parse args from the cli
    parser = create_parser(htb_client)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
