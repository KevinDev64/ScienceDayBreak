#!/usr/bin/env python3

import os

def execute_com(command):
	code = os.system(command)
	if code != 0:
		print(f"Failed with code {code} when running the command `{command}`")
		exit(1)

result_codes = []
commands = [
	"git fetch",
	"git pull",
	"docker compose pull",
	"docker compose down",
	"docker compose up -d"
]

for command in commands:
	execute_com(command)

print("Updater -> SUCCESS!")
