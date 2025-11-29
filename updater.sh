#!/usr/bin/env python3

import os
import subprocess

def execute_com(command):
	if command == "git pull":
		result = subprocess.check_output(command, shell=True)
		if result == b'Already up to date.\n':
			print("Updater! -> NO UPDATES!")
			exit(0)
	else:
		code = os.system(command)
		if code != 0:
			print(f"Failed with code {code} when running the command `{command}`")
			exit(1)

result_codes = []
commands = [
	"git fetch",
	"git pull origin main",
	"docker compose pull",
	"docker compose down",
	"docker compose up -d"
]


for command in commands:
	execute_com(command)

print("Updater -> SUCCESS!")
