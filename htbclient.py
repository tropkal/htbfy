import argparse
import os
import requests
import sys
import time

from datetime import datetime, timezone
from pwn import log
from pwnlib.log import Progress
from tabulate import tabulate
from typing import Optional

JSON = (
        str
        | int
        | float
        | bool
        | None
        | dict[str, "JSON"]  # nested objects
        | list["JSON"]  # arrays
        )


class HTBClient:
    def __init__(self, app_token: str) -> None:
        self.app_token = app_token
        self.base_url = "https://labs.hackthebox.com/api/v4"
        self.session = requests.Session()
        self.check_time = False

    def _build_headers(self) -> dict[str, str]:
        headers = {
                "Authorization": f"Bearer {self.app_token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
                }

        return headers

    def get_connection_status(self) -> None:
        url = f"{self.base_url}/user/connection/status"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:
            status = response.json()["status"]
            if status:
                log.success("Connected to the VPN.")
                ipv4 = response.json()["connection"]["ip4"]
                ipv6 = response.json()["connection"]["ip6"]
                print(f"IPv4: {ipv4}, IPv6: {ipv6}")
            else:
                log.failure("Not connected to the VPN.")

    def seasonal_user_rank(self) -> None:
        url = f"{self.base_url}/season/user/rank"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:
            print()
            print("Seasonal rank info:")
            print("-------------------")
            for k, v in response.json()["data"].items():
                print(f"{k.capitalize()}: {v}")
            print()
        else:
            log.failure("Could not fetch the seasonal rank information.")

    def get_user_info(
            self,
            ) -> None:
        url = f"{self.base_url}/user/info"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:
            print()
            print("User info:")
            print("-----------------")
            for k, v in response.json()["info"].items():
                print(f"{k.capitalize()}: {v}")
            print()
        else:
            log.failure("Could not fetch my user's information.")

    # private function for internal use only
    # NOT IN THE MOOD TO REMOVE THIS ONE OR THE OTHER ONE
    def _get_active_machine(self) -> JSON | None:
        url = f"{self.base_url}/machine/active"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:
            info_obj = response.json()["info"]
            if info_obj is not None:
                return info_obj
            else:
                log.info("No active machine found.")
                return None
        else:
            log.failure("Failed to fetch the active machine.")
            return None

    def _format_time(self, date_obj: datetime) -> str:

        # date.days
        # AttributeError: 'str' object has no attribute 'days'
        days, seconds = date_obj.days, date_obj.seconds
        hours = days * 24 + seconds // 3600
        minutes = seconds % 3600 // 60
        seconds = seconds % 60

        return "{:02}h:{:02}m:{:02}s".format(hours, minutes, seconds)

    def _convert_time_to_utc(
            self,
            info_obj: JSON,
            machine_os: str = "",
            ) -> None:
        date_format = "%Y-%m-%d %H:%M:%S"
        initial_expires_at = datetime.strptime(
                info_obj["expires_at"], date_format
                ).replace(tzinfo=timezone.utc)

        time_now_utc = datetime.now(timezone.utc)
        time_left = initial_expires_at - time_now_utc

        # WHATS time_left ??
        breakpoint()
        formatted_time_left = self._format_time(time_left)

        if self.check_time:
            # get the new expires_at time after extending the box's time
            info_obj = self._get_active_machine()
            if info_obj is None:
                log.failure("No active machine found.")
                sys.exit(-1)

            new_expires_at = datetime.strptime(
                    info_obj["expires_at"], date_format
                    ).replace(tzinfo=timezone.utc)

            time_added = new_expires_at - initial_expires_at
            new_expires_at = new_expires_at.strftime("%Y-%m-%d %H:%M:%S") # change the format
            time_added_formatted = self._format_time(time_added)
            time_remaining = time_added_formatted + formatted_time_left
            formatted_time_remaining = self._format_time(time_remaining)

            log.info(
                    f"Expires at: {new_expires_at} UTC, time left before extending: {formatted_time}, {time_added} more hours added to the clock, total time remaining: {formatted_time_remaining}"
                    )
        else:
            log.info(
                    f"Currently active machine: {info_obj['name']}, OS: {machine_os}, IP: {info_obj['ip']}, time left: {formatted_time_left}."
                    )

    def get_active_machine(self) -> None:
        # NOT IN THE MOOD TO REMOVE THIS ONE OR THE OTHER ONE
        url = f"{self.base_url}/machine/active"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:
            info_obj = response.json()["info"]
            if info_obj is not None:
                machine_name = info_obj["name"]
                machine_profile = self._get_machine_profile(machine_name)["info"]
                machine_os = machine_profile["os"]
                # convert local time to UTC
                self._convert_time_to_utc(info_obj, machine_os)
            else:
                log.info("No active machine found.")
        else:
            log.failure("Failed to fetch the active machine.")

    def _pretty_print(
            self, machine_profile_list: list[JSON], p: Optional[Progress] = None
            ) -> None:
        if p is not None:
            p.status("Please wait...")

        # building the table entries, i.e. each machine's profile
        rows = [
                [
                    idx,
                    machine_profile.get("name"),  # name
                    machine_profile.get("os"),  # os
                    machine_profile.get("difficultyText"),  # difficulty
                    datetime.strptime(
                        machine_profile.get("release").split("T")[0],
                        "%Y-%m-%d",
                        ).date(),  # date
                    machine_profile.get("stars"),  # rating
                    machine_profile.get("playInfo", {}).get("isActive"),  # running
                    machine_profile.get("playInfo", {}).get(
                        "active_player_count"
                        ),  # active player count
                    machine_profile.get(
                        "points"
                        ),  # what's the diff between this and static_points ?
                    machine_profile.get("retired"),  # retired
                    machine_profile.get("user_owns_count"),  # total user owns
                    machine_profile.get("root_owns_count"),  # total root owns
                    machine_profile.get("authUserInUserOwns"),  # owned user
                    machine_profile.get("authUserInRootOwns"),  # owned root
                    ]
                for idx, machine_profile in enumerate(machine_profile_list, 1)
                ]

        if p is not None:
            p.success("Success!")

        # populating the table
        print(
                tabulate(
                    rows,
                    headers=[
                        "ID",
                        "Name",
                        "OS",
                        "Diff.",
                        "Released",
                        "Rating",
                        "Running",
                        "Players",
                        "Points",
                        "Retired",
                        "User owns",
                        "Root owns",
                        "User",
                        "Root",
                        ],
                    tablefmt="pretty",
                    )
                )
        print()

    def get_active_machines(self, diff, os) -> None:
        diff_machine_profile_list = []
        os_machine_profile_list = []

        if diff:
            diff = diff.capitalize()
            log.info(f"Filtering by '{diff.capitalize()}' difficulty.")

        if os:
            os = os.capitalize()
            log.info(f"Filtering by OS.")

        url = f"{self.base_url}/machine/paginated?per_page=100"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:
            machine_list = response.json()["data"]

            p = log.progress("Fetching the list of active machines...")
            p.status("Please wait...")
            machine_profile_list = []
            for machine_info in machine_list:
                machine_name = machine_info.get("name")
                try:
                    machine_profile = self._get_machine_profile(machine_name)["info"]
                    if diff and machine_info["difficultyText"] == diff:
                        diff_machine_profile_list.append(machine_profile)
                    elif os and machine_info["os"] == os:
                        os_machine_profile_list.append(machine_profile)
                    else:
                        machine_profile_list.append(machine_profile)

                except TypeError:
                    log.warning("Rate limit exceeded, aborting.")
                    sys.exit(-1)

            if diff_machine_profile_list:
                self._pretty_print(diff_machine_profile_list, p)
            elif os_machine_profile_list:
                self._pretty_print(os_machine_profile_list, p)
            elif machine_profile_list:
                self._pretty_print(machine_profile_list, p)
        else:
            log.failure("Could not fetch the list of active machines.")

    def _get_machine_profile(self, machine_name: str) -> JSON:
        url = f"{self.base_url}/machine/profile/{machine_name}"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            return
        elif response.status_code == 404 and response.json()["message"] == "Machine not found":
            log.failure("There's no machine with that name.")
            sys.exit(-1)
        else:
            log.failure("Could not fetch the machine's profile.")

    def terminate_active_machine(self) -> None:
        url = f"{self.base_url}/vm/terminate"
        machine_name_json = self._get_active_machine()
        if machine_name_json is None:
            log.failure("There's no machine to terminate.")
            sys.exit(-1)
        try:
            machine_id = machine_name_json["id"]
        except TypeError:
            log.failure("Could not fetch the machine's ID for termination.")
            sys.exit(-1)

        data = {"machine_id": machine_id}
        response = self.session.post(url, data=data, headers=self._build_headers())
        try:
            if response.status_code == 200 and response.json()["success"] == True:
                log.success("Machine terminated successfully.")
            else:
                log.failure("Something went wrong while terminating the machine.")
                sys.exit(-1)
        except TypeError:
            log.failure("Could not terminate machine.")

    def _get_spawn_status(self) -> None:
        # check if the machine spawned successfully, otherwise wait 10s and try again
        response_json = self._get_active_machine()
        if response_json is None:
            log.failure("Failed to fetch the status of the machine.")
            sys.exit(-1)
        if response_json["isSpawning"] == True:
            time.sleep(10)
            self._get_spawn_status()

    def spawn_machine(self, machine_name_obj) -> None:
        url = f"{self.base_url}/vm/spawn"
        machine_name = machine_name_obj.name
        if machine_name[0].isdigit():
            log.failure("The name of the box must be a string.")
            sys.exit(-1)
        machine_profile_json = self._get_machine_profile(machine_name)
        machine_id = machine_profile_json["info"]["id"]
        machine_name = machine_profile_json["info"]["name"]
        data = {"machine_id": machine_id}
        time_start = time.time()
        response = self.session.post(url, data=data, headers=self._build_headers())
        if response.status_code == 200 and response.json()["success"] == True:
            p = log.progress(f"Machine {machine_name} is spawning.")
        elif response.status_code == 403:
            log.warning(
                    f"Machine {machine_name} is spawning or already active. Terminate that machine first and then spawn another."
                    )
            sys.exit(-1)
        else:
            log.failure(f"Could not spawn machine {machine_name}.")
            sys.exit(-1)

        p.status("Please wait...")
        self._get_spawn_status()
        info_obj = self._get_active_machine()
        if info_obj is not None:
            machine_ip = info_obj["ip"]
            time_end = time.time()
            spawn_time = time_end - time_start
            p.success()
            log.success(
                    f"Machine spawned successfully, its IP is: {machine_ip}. Took {spawn_time:.2f} seconds."
                    )
        else:
            log.failure(
                    f"Could not query the spawn status of the machine {machine_name}."
                    )
            sys.exit(-1)

    def reset_machine(self) -> None:
        url = f"{self.base_url}/vm/reset"
        info_obj = self._get_active_machine()
        if info_obj is None:
            log.failure(f"No active machine found.")
            sys.exit(-1)

        machine_id = info_obj["id"]
        machine_name = info_obj["name"]
        data = {"machine_id": machine_id}
        time_start = time.time()
        try:
            response = self.session.post(url, data=data, headers=self._build_headers())
            if response.status_code == 200 and response.json()["success"] == True:
                p = log.progress(f"Machine {machine_name} is resetting.")
            elif response.status_code == 500:
                log.warning("Machine is already resetting.")
                sys.exit(-1)
            else:
                log.warning(f"Failed to reset machine {machine_name}.")
                sys.exit(-1)
        except Exception as e:
            # print(e)
            log.warning(
                    f"Some unexpected error occurred while resetting the machine {machine_name}."
                    )
            sys.exit(-1)

        p.status("Please wait...")
        self._get_spawn_status()
        time_end = time.time()
        spawn_time = time_end - time_start
        p.success()
        log.success(f"Machine got reset successfully. Took {spawn_time:.2f} seconds.")

    def extend_machine_time(self) -> None:
        url = f"{self.base_url}/vm/extend"
        info_obj = self._get_active_machine()
        if info_obj is None:
            log.failure("No active machine found.")
            sys.exit(-1)

        machine_id = info_obj["id"]
        data = {"machine_id": machine_id}
        initial_expiration_time = info_obj["expires_at"]

        response = self.session.post(url, data=data, headers=self._build_headers())
        if response.status_code == 200:
            if response.json()["success"] == True:
                self.check_time = True
                log.success("Machine time extended successfully.")

                self._convert_time_to_utc(
                        info_obj,
                        )
        else:
            log.failure(
                    "Failed to extend the machine's time, it has plenty until expiration."
                    )
            log.info(
                    f"You could run './{os.path.basename(__file__)} machine active' to check the actual time until expiration."
                    )

    def submit_flag(self, flag_obj: argparse.Namespace) -> None:
        url = f"{self.base_url}/machine/own"
        info_obj = self._get_active_machine()
        if info_obj is None:
            log.warning("Need an active machine to submit a flag.")
            sys.exit(0)

        machine_id = int(info_obj["id"])
        flag = str(flag_obj.flag)
        # rewrite the api version for this request, because apparently this is using v5
        url = url.replace("v4", "v5")

        data = {"flag": flag, "id": machine_id}

        response = self.session.post(url, json=data, headers=self._build_headers())
        if (
                response.status_code == 200
                and response.json()["success"] == True
                and "You pwned the " in response.json()["message"]
                ):
            log.success("Flag submitted successfully!")
        elif (
                response.status_code == 400
                and response.json()["message"] == "Incorrect Flag."
                ):
            log.failure("Already submitted this flag or it's incorrect.")
        else:
            log.failure("Something bad happened when submitting the flag.")

    def _discover(self, machine_id: int, owned: str) -> tuple[int | None, bool]:
        url = f"{self.base_url}/machines/{machine_id}/adventure"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:  # there already exists a rating
            if owned == "user":
                if (
                        response.json()["data"][0]["completed"] == True
                        and response.json()["data"][0]["flag_rating"] is not None
                        ):
                    existing_rating = int(
                            response.json()["data"][0]["flag_rating"]
                            )  # user rating
                    return existing_rating, True
                elif (
                        response.json()["data"][1]["completed"] == True
                        and response.json()["data"][1]["flag_rating"] is None
                        ):
                    return None, True
                else:
                    return None, False

            elif owned == "root":
                if (
                        response.json()["data"][1]["completed"] == True
                        and response.json()["data"][1]["flag_rating"] is not None
                        ):
                    existing_rating = int(
                            response.json()["data"][1]["flag_rating"]
                            )  # root rating
                    return existing_rating, True
                elif (
                        response.json()["data"][1]["completed"] == True
                        and response.json()["data"][1]["flag_rating"] is None
                        ):
                    return None, True
                else:
                    return None, False
        else:
            log.failure("Something bad happened when fetching the rating.")
            return None, False

    def rate_flag(self, rating_namespace: argparse.Namespace) -> None:
        rating_choices = {
                2: "very easy",
                3: "easy",
                4: "not too easy",
                5: "medium",
                6: "a bit hard",
                7: "hard",
                8: "too hard",
                9: "extremely hard",
                10: "brainfuck",
                }

        owned = str(rating_namespace.owned)
        rate = rating_namespace.rating

        if owned not in ("user", "root"):
            log.failure(
                    "Can only submit flag difficulty ratings for user or root."
                    )
            sys.exit(-1)

        try:
            rate = int(rate)
        except ValueError:
            log.failure(f"Rating must be an integer between 1 and 10.")
            sys.exit(-1)

        if rate < 1 or rate > 10:
            log.failure(f"Can't give a rating score below 1 or above 10, try again.")
            sys.exit(-1)

        # find the active machine's id
        machine_name_json = self._get_active_machine()
        if machine_name_json is None:
            log.failure("There's no machine to query.")
            sys.exit(-1)
        try:
            machine_id = machine_name_json["id"]
            machine_name = machine_name_json["name"]
        except TypeError:
            log.failure("Could not fetch the machine's ID. ")
            sys.exit(-1)

        # checking if there is an already submitted rating for a given flag
        existing_rating, completed = self._discover(machine_id, owned)
        if completed and isinstance(existing_rating, int):
            log.info(
                    f"{owned.capitalize()} flag has already been rated as '{rating_choices[existing_rating].capitalize()}' ({existing_rating}) for {machine_name}."
                    )
            sys.exit(-1)

        if completed and not existing_rating:
            url = f"{self.base_url}/machine/{machine_id}/flag/rate"
            data = {"difficulty": rate, "machineId": machine_id, "type": owned}
            response = self.session.post(url, json=data, headers=self._build_headers())
            if (
                    response.status_code == 200
                    and response.json()["message"] == "Flag rated."
                    ):
                log.success(
                        f"{owned.capitalize()} flag rated successfully as '{rating_choices[rate].capitalize()}' ({rate}) for {machine_name}."
                        )
        else:
            log.failure("Can't submit a rating for a flag that was not found yet.")
            sys.exit(-1)

    def search_machine(self, machine_namespace: argparse.Namespace) -> None:
        machine_name = machine_namespace.name
        if machine_name[0].isdigit():
            log.failure("The name of the box must be a string.")
            sys.exit(-1)

        url = f"{self.base_url}/search/fetch?query={machine_name}"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:
            try:
                machine_profile = self._get_machine_profile(machine_name)["info"]
                machine_list = []
                machine_list.append(machine_profile)

                if machine_list:
                    self._pretty_print(machine_list)
            except TypeError:  # machine not found because it doesn't exist
                log.failure("Machine not found.")

    def _search_user_profile(self, user_id: int) -> JSON:
        url = f"{self.base_url}/user/profile/basic/{user_id}"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:
            return response.json()
        else:
            log.failure("Could not fetch the requested user's information.")
            sys.exit(-1)

    def search_user(self, username_obj: argparse.Namespace) -> None:
        username = username_obj.name
        url = f"{self.base_url}/search/fetch?query={username}"
        response = self.session.get(url, headers=self._build_headers())
        if response.status_code == 200:
            try:
                user_id = int(response.json()["users"][0]["id"])
                user_profile = self._search_user_profile(user_id)
                print()
                print("User info:")
                print("----------")
                for k, v in user_profile["profile"].items():
                    print(f"{k.capitalize()}: {v}")
                print()
            except KeyError:
                log.failure("Could not fetch the requested user's information.")
        else:
            log.failure("Could not fetch the requested user's information.")
