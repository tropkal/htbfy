# htbfy
➔ CLI client for the HackTheBox API.

# Why ?
Because I hate leaving my terminal. The terminal is love, the terminal is life. Amen. Accept it. Embrace it. Thank me later.  
Also, I'm a hacker, not a professional programmer. My code could probably be cleaner and more efficient, whatever, if it works, it works.

# HTB app token
This script uses **dotenv** to load the HTB app token in an environment variable called **HTB_APP_TOKEN**. You can get yours from your HTB profile/profile settings, create app token. It's only available for 1 year max, so be mindful of that. Put the app token in the .env file under the same directory as this script.  
```
$ ls -a
.  ..  .env  .git  .gitignore  README.md  requirements.txt
$ cat .env
HTB_APP_TOKEN=your_app_token_here
```

# Installation
## Using python3's venv module
```
$ git clone https://github.com/tropkal/htbfy
$ cd htbfy  
$ python3 -m venv venv  
$ . venv/bin/activate  
$ pip install -r requirements.txt
```
## Using uv
```
$ git clone https://github.com/tropkal/htbfy  
$ cd htbfy  
$ uv venv venv
$ . venv/bin/activate  
$ uv pip install -r requirements.txt
```
# Usage
This script is by no means complete when it comes to the HTB API, but it can do some basic things (at least for now), like spawning, terminating, resetting, extending a machine's time, submitting a flag. It can also fetch: the current seasonal rank, a list of the active machines, the current active machine and the time left on it, the connection status of the VPN, and it can also search for any machine and retrieve some information on it like its OS, difficulty, or search for a particular user.

I'll maybe add functionality later regarding challenges, fortresses and/or whatever else. Maybe. For now, this works for me.
```
$ ./htbfy.py -h
usage: htbfy.py [-h] {user,machine} ...

HackTheBox API Client

positional arguments:
{user,machine}
user          User subcommands.
machine       Machine subcommands.

options:
-h, --help      show this help message and exit
```
## User API
```
$ ./htbfy.py user -h
usage: htbfy.py user [-h] {info,status,rank,search} ...

positional arguments:
{info,status,rank,search}
info                Get user information.
status              Get connection status.
rank                Get seasonal rank.
search              Search for a particular user.

options:
-h, --help            show this help message and exit
```
## Machine API
```
$ ./htbfy.py machine -h
usage: htbfy.py machine [-h] {active,list,spawn,terminate,reset,extend,submit,search} ...

positional arguments:
{active,list,spawn,terminate,reset,extend,submit,search}
active              Get the currently active machine.
list                Get a list of the currently active machines.
spawn               Spawn a machine.
terminate           Terminate the currently active machine.
reset               Reset the currently active machine.
extend              Extend the currently active machine's time.
submit              Submit a flag.
search              Search for a particular machine.

options:
-h, --help            show this help message and exit
```
## Examples
Spawning a machine:
```
$ ./htbfy.py machine spawn darkcorp
[+] Machine DarkCorp is spawning.
[+] Machine spawned successfully, its IP is: 10.129.232.7. Took 102.73 seconds.
```
Listing the currently active machine:
```
$ ./htbfy.py machine active
➔  Currently active machine: DarkCorp, IP: 10.129.232.7, time left: 23h:57m:15s.
```
Searching for a particular machine:
```
$ ./htbfy.py machine search darkcorp
+----+----------+---------+--------+------------+--------+---------+---------+--------+---------+-----------+-----------+------+-------+
| ID |   Name   |   OS    | Diff.  |  Released  | Rating | Running | Players | Points | Retired | User owns | Root owns | User | Root  |
+----+----------+---------+--------+------------+--------+---------+---------+--------+---------+-----------+-----------+------+-------+
| 1  | DarkCorp | Windows | Insane | 2025-02-08 |  4.8   |  False  |    0    |   50   |  False  |   1544    |   1529    | True | False |
+----+----------+---------+--------+------------+--------+---------+---------+--------+---------+-----------+-----------+------+-------+
```
Terminating a machine:
```
$ ./htbfy.py machine terminate
[+] Machine terminated successfully.
```
Submitting a flag:
```
$ ./htbfy.py machine submit someflag
[+] Flag submitted successfully!
```
Listing all 20 active machines:
```
$ ./htbfy.py machine list
[+] Fetching the list of active machines...: Success!
+----+-------------+---------+--------+------------+--------+---------+---------+--------+---------+-----------+-----------+-------+-------+
| ID |    Name     |   OS    | Diff.  |  Released  | Rating | Running | Players | Points | Retired | User owns | Root owns | User  | Root  |
+----+-------------+---------+--------+------------+--------+---------+---------+--------+---------+-----------+-----------+-------+-------+
| 1  | Expressway  |  Linux  |  Easy  | 2025-09-20 |  3.6   |  False  |    0    |   20   |  False  |   3701    |   3497    | False | False |
| 2  |   HackNet   |  Linux  | Medium | 2025-09-13 |  3.6   |  False  |    0    |   30   |  False  |   1098    |    893    | False | False |
| 3  |  Soulmate   |  Linux  |  Easy  | 2025-09-06 |  3.1   |  False  |    0    |   20   |  False  |   3187    |   3068    | False | False |
| 4  |  Guardian   |  Linux  |  Hard  | 2025-08-30 |  4.9   |  False  |    0    |   40   |  False  |   1035    |    963    | False | False |
| 5  |  Previous   |  Linux  | Medium | 2025-08-23 |  4.4   |  False  |    0    |   30   |  False  |   2352    |   2131    | True  | True  |
| 6  | CodePartTwo |  Linux  |  Easy  | 2025-08-16 |  4.4   |  False  |    0    |   20   |  False  |   5791    |   5386    | True  | True  |
| 7  | Cobblestone |  Linux  | Insane | 2025-08-09 |  3.1   |  False  |    0    |   50   |  False  |   1404    |   1322    | False | False |
| 8  |   Editor    |  Linux  |  Easy  | 2025-08-02 |  4.2   |  False  |    0    |   20   |  False  |   7949    |   7283    | True  | True  |
| 9  |     Era     |  Linux  | Medium | 2025-07-26 |  3.2   |  False  |    0    |   30   |  False  |   3196    |   2786    | True  | True  |
| 10 |   Mirage    | Windows |  Hard  | 2025-07-19 |  4.2   |  False  |    0    |   40   |  False  |   2035    |   1686    | True  | True  |
| 11 |  Outbound   |  Linux  |  Easy  | 2025-07-12 |  3.7   |  False  |    0    |   20   |  False  |   7177    |   6493    | True  | True  |
| 12 |   Voleur    | Windows | Medium | 2025-07-05 |  4.8   |  False  |    0    |   30   |  False  |   3460    |   2977    | True  | True  |
| 13 |  RustyKey   | Windows |  Hard  | 2025-06-28 |  4.3   |  False  |    0    |   40   |  False  |   2177    |   1750    | True  | True  |
| 14 | Artificial  |  Linux  |  Easy  | 2025-06-21 |  4.2   |  False  |    0    |   20   |  False  |   8102    |   6619    | True  | True  |
| 15 |   Sorcery   |  Linux  | Insane | 2025-06-14 |  4.6   |  False  |    0    |   50   |  False  |   1085    |   1019    | False | False |
| 16 | TombWatcher | Windows | Medium | 2025-06-07 |  4.5   |  False  |    0    |   30   |  False  |   4739    |   3944    | True  | True  |
| 17 | Certificate | Windows |  Hard  | 2025-05-31 |   4    |  False  |    0    |   40   |  False  |   2741    |   2621    | True  | True  |
| 18 |    Puppy    | Windows | Medium | 2025-05-17 |  4.8   |  False  |    0    |   30   |  False  |   6047    |   5538    | True  | True  |
| 19 | WhiteRabbit |  Linux  | Insane | 2025-04-05 |  3.9   |  False  |    0    |   50   |  False  |   1900    |   1862    | False | False |
| 20 |  DarkCorp   | Windows | Insane | 2025-02-08 |  4.8   |  False  |    0    |   50   |  False  |   1544    |   1529    | True  | False |
+----+-------------+---------+--------+------------+--------+---------+---------+--------+---------+-----------+-----------+-------+-------+
```
Fetching the VPN status:
```
$ ./htbfy.py user status
[+] Connected to the VPN.
IPv4: 10.10.14.161, IPv6: dead:beef:2::109f
```
Fetching the seasonal rank:
```
$ ./htbfy.py user rank

Seasonal rank info:
-------------------
League: None
Rank: None
Next_rank: {'id': 1, 'title': 'Bronze', 'requirement': 0}
Total_ranks: None
Rank_suffix: None
Total_season_points: 0
Flags_to_next_rank: {'obtained': 0, 'total': 1}
```
