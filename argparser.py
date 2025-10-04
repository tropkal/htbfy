import argparse

from htbclient import HTBClient


def create_parser(htb_client: HTBClient) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HackTheBox API Client")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # user API
    user_parser = subparsers.add_parser("user", help="User subcommands.")
    user_subcommand = user_parser.add_subparsers(dest="action", required=True)

    user_info = user_subcommand.add_parser("info", help="Get user information.")
    user_info.set_defaults(func=lambda _: htb_client.get_user_info())

    connection_status = user_subcommand.add_parser(
        "status", help="Get connection status."
    )
    connection_status.set_defaults(func=lambda _: htb_client.get_connection_status())

    seasonal_rank = user_subcommand.add_parser("rank", help="Get seasonal rank.")
    seasonal_rank.set_defaults(func=lambda _: htb_client.seasonal_user_rank())

    search_user = user_subcommand.add_parser(
        "search", help="Search for a particular user."
    )
    search_user.add_argument("name", help="Name of the user.")
    search_user.set_defaults(func=htb_client.search_user)

    # machine API
    machine_parser = subparsers.add_parser("machine", help="Machine subcommands.")
    machine_subcommand = machine_parser.add_subparsers(dest="action", required=True)

    active_machine = machine_subcommand.add_parser(
        "active", help="Get the currently active machine."
    )
    active_machine.set_defaults(func=lambda _: htb_client.get_active_machine())

    active_machines = machine_subcommand.add_parser(
        "list",
        help="Get a list of the currently active machines (-diff to filter by a particular difficulty).",
    )
    active_machines.add_argument(
        "-diff",
        required=False,
        default="",
        help="Difficulty to filter the list of active machines by.",
    )
    active_machines.add_argument(
        "-os",
        required=False,
        default="",
        help="OS to filter the list of active machines by.",
    )
    active_machines.set_defaults(
        func=lambda args: htb_client.get_active_machines(diff=args.diff, os=args.os)
    )

    spawn_machine = machine_subcommand.add_parser("spawn", help="Spawn a machine.")
    spawn_machine.add_argument("name", help="Name of the machine to spawn.")
    spawn_machine.set_defaults(func=htb_client.spawn_machine)

    terminate_machine = machine_subcommand.add_parser(
        "terminate", help="Terminate the currently active machine."
    )
    terminate_machine.set_defaults(func=lambda _: htb_client.terminate_active_machine())

    reset_machine = machine_subcommand.add_parser(
        "reset", help="Reset the currently active machine."
    )
    reset_machine.set_defaults(func=lambda _: htb_client.reset_machine())

    extend_machine = machine_subcommand.add_parser(
        "extend", help="Extend the currently active machine's time."
    )
    extend_machine.set_defaults(func=lambda _: htb_client.extend_machine_time())

    flag_machine = machine_subcommand.add_parser("submit", help="Submit a flag.")
    flag_machine.add_argument("flag", help="Flag to be submitted.")
    flag_machine.set_defaults(func=htb_client.submit_flag)

    search_machine = machine_subcommand.add_parser(
        "search", help="Search for a particular machine."
    )
    search_machine.add_argument("name", help="Name of the machine.")
    search_machine.set_defaults(func=htb_client.search_machine)

    rate_machine = machine_subcommand.add_parser(
        "rate", help="Submit a difficulty rating for an owned flag."
    )
    rate_machine.add_argument(
        "owned",
        help="Submit a difficulty rating for an owned flag for the currently active machine, i.e. user | root.",
    )
    rate_machine.add_argument("rating", help="Rating to submit, between 1 and 10.")
    rate_machine.set_defaults(func=htb_client.rate_flag)

    return parser
