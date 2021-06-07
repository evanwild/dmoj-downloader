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
EXCLUDE_CHARS = '\\/:*?"<>|'

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
			print(f'{ERROR_PREFIX} No problem exists with code {self.problem}')
			return

		data = r.json()
		name = ''.join(c for c in data['name'] if c not in EXCLUDE_CHARS)
		group = f'result/{data["group"]}'

		if not os.path.isdir(group):
			os.mkdir(group)
			print(f'{INFO_PREFIX} Created {group} folder')

		shutil.copyfile(self.filepath, f'{group}/{name}.{self.extension}')


def keep_newest(solutions: list) -> list:
	# Make sure earlier submissions come earlier in the list
	solutions = sorted(solutions, key=lambda solution: int(solution.id_))

	# Only keep the last solution for each problem
	unique = {solution.problem: solution for solution in solutions}

	return list(unique.values())


def main() -> None:

	# This line makes color escape sequences magically work in cmd/powershell
	os.system('color')

	if len(sys.argv) != 2:
		sys.exit(f'{ERROR_PREFIX} Please specify the directory to your solutions')

	old_dir = sys.argv[1]

	if not os.path.isdir(old_dir):
		sys.exit(f'{ERROR_PREFIX} That directory does not exist')

	filenames = os.listdir(old_dir)

	if not os.path.isfile(f'{old_dir}/info.json'):
		sys.exit(f'{ERROR_PREFIX} The info.json file does not exist in that directory')

	filenames.remove('info.json')
	info_file = open(f'{old_dir}/info.json')
	info = json.load(info_file)
	info_file.close()
		
	if not os.path.isdir('result'):
		os.mkdir('result')
		print(f'{INFO_PREFIX} Created result folder')

	solutions = []
	for filename in filenames:
		filepath = f'{old_dir}/{filename}'
		id_, extension = filename.split('.')
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