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


@dataclass
class Solution:
	filepath: str
	id_: str
	extension: str
	problem: str

	def process(self) -> None:
		url = f'https://dmoj.ca/api/problem/info/{self.problem}'
		r = requests.get(url)

		if not r.ok:
			print(f'ERROR: No problem exists with code {self.problem}')
			return

		data = r.json()
		name = ''.join(c for c in data['name'] if c not in EXCLUDE_CHARS)
		group = f'result/{data["group"]}'

		if not os.path.isdir(group):
			os.mkdir(group)
			print(f'INFO: Created {group} folder')

		shutil.copyfile(self.filepath, f'{group}/{name}.{self.extension}')


def keep_newest(solutions: list) -> list:
	# Make sure earlier submissions come earlier in the list
	solutions = sorted(solutions, key=lambda solution: int(solution.id_))

	# Only keep the last solution for each problem
	unique = {solution.problem: solution for solution in solutions}

	return list(unique.values())


def main() -> None:
	if len(sys.argv) != 2:
		sys.exit('ERROR: Please specify the directory to your solutions')

	old_dir = sys.argv[1]

	if not os.path.isdir(old_dir):
		sys.exit('ERROR: That directory does not exist')

	filenames = os.listdir(old_dir)

	if not os.path.isfile(f'{old_dir}/info.json'):
		sys.exit('ERROR: The info.json file does not exist in that directory')

	filenames.remove('info.json')
	info_file = open(f'{old_dir}/info.json')
	info = json.load(info_file)
	info_file.close()
		
	if not os.path.isdir('result'):
		os.mkdir('result')
		print('INFO: Created result folder')

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
		print(f'INFO: Finished {solution.problem} - {done}/{len(solutions)}')
		time.sleep(60 / API_CALLS_PER_MIN)


if __name__ == '__main__':
	main()
