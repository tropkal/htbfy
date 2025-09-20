# htbfy
➔ CLI client for the HackTheBox API.

# Why ?
Because I hate leaving my terminal. The terminal is love, the terminal is life. Amen. Accept it. Embrace it. Thank me later.  
Also, I'm a hacker, not a professional programmer. My code could probably be more efficient and cleaner, whatever, if it works, it works.

# HTB app token
This script uses **dotenv** to load the HTB app token in an environment variable called **HTB_APP_TOKEN**. You can get yours from your HTB profile/profile settings, create app token. It's only available for 1 year max, so be mindful of that. Put the app token in the .env file under the same directory as this script.  
```
$ ls
.env htbfy.py
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
This script is by no means complete when it comes to the HTB API, but it can do some basic things (at least for now), like spawning, terminating, resetting, extending a machine's time. It can also fetch: the current seasonal rank, a list of the active machines, the current active machine and the time left on it, the connection status of the VPN, and it can also search for any machine and retrieve some information on it like its OS, difficulty, etc.

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
usage: htbfy.py user [-h] {info,status,rank} ...

positional arguments:
{info,status,rank}
info              Get user information.
status            Get connection status.
rank              Get seasonal rank.

options:
-h, --help          show this help message and exit
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
