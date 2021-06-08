from dataclasses import dataclass
import json
import os
import requests
import shutil
import sys
import time


# Do not exceed 90 or you will be captcha'd
API_CALLS_PER_MIN = 85

# Some characters are not allowed in file names so they will be ignored
FILENAME_EXCLUDE = '\\/:*?"<>|'

# Prefixes for outputting colour to the console
ERROR_PREFIX = '\033[1;41m ERROR \033[1;m'
INFO_PREFIX = '\033[1;44m INFO \033[1;m'
DONE_PREFIX = '\033[1;42m DONE \033[1;m'


@dataclass
class Solution:
	filepath: str
	id_: str
	extension: str
	problem: str

	def process(self) -> None:
		r = requests.get(f'https://dmoj.ca/api/problem/info/{self.problem}')

		if not r.ok:
			print(f'{ERROR_PREFIX} No problem exists named {self.problem}')
			return

		data = r.json()
		name = ''.join(c for c in data['name'] if c not in FILENAME_EXCLUDE)
		group = f'result/{data["group"]}'

		try:
			os.mkdir(group)
			print(f'{INFO_PREFIX} Created {group} folder')
		except FileExistsError:
			pass

		shutil.copyfile(self.filepath, f'{group}/{name}.{self.extension}')


def keep_newest(solutions: list) -> list:
	solutions.sort(key=lambda solution: int(solution.id_)) # Sort old to new
	unique = {solution.problem: solution for solution in solutions}

	return list(unique.values())


def main() -> None:
	os.system('color') # Makes colors work in cmd/powershell

	old_dir = ''
	try:
		old_dir = sys.argv[1]
	except IndexError:
		sys.exit(f'{ERROR_PREFIX} Please specify the solution directory')

	files = []
	try:
		files = os.listdir(old_dir)
	except FileNotFoundError:
		sys.exit(f'{ERROR_PREFIX} That directory does not exist')

	info = {}
	try:
		with open(f'{old_dir}/info.json') as info_file:
			info = json.load(info_file)
	except FileNotFoundError:
		sys.exit(f'{ERROR_PREFIX} That directory does not have an info.json')

	try:
		os.mkdir('result')
		print(f'{INFO_PREFIX} Created result folder')
	except FileExistsError:
		pass

	solutions = []
	for file in files:
		if file != 'info.json':
			filepath = f'{old_dir}/{file}'
			id_, extension = file.split('.')
			problem = info[id_]['problem']
			solutions.append(Solution(filepath, id_, extension, problem))
	
	solutions = keep_newest(solutions)

	done = 0
	for solution in solutions:
		solution.process()
		done += 1
		print(f'{DONE_PREFIX} {solution.problem} - {done}/{len(solutions)}')
		time.sleep(60 / API_CALLS_PER_MIN)


if __name__ == '__main__':
	main()