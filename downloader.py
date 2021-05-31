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

# Data included in the DMOJ download that tracks what problem each solution is for
info = {}

# The supplied directory which stores all the solution files
solution_dir = ''



def get_problem_data(problem):
	url = f'https://dmoj.ca/api/v2/problem/{problem}'
	r = requests.get(url)
	data = r.json()['data']['object']
	return data


def make_category_path(category):
	path = f'result/{category}'
	if not os.path.exists(path):
		os.mkdir(path)


def process(problem, file):
	try:
		data = get_problem_data(problem)

		name = data['name']
		for char in EXCLUDE_CHARS:
			name = name.replace(char, '')

		category = data['group']
		make_category_path(category)

		ext = file.split('.')[1]

		old_dir = f'{solution_dir}/{file}'
		new_dir = f'result/{category}/{name}.{ext}'

		shutil.copyfile(old_dir, new_dir)

	except:
		print(f'ERROR: No problem {problem}')


def is_latest(a, b):
	a_num = int(a.split('.')[0])
	b_num = int(b.split('.')[0])
	return a_num > b_num


def keep_most_recent(solutions):
	result = {}
	for solution in solutions:
		if solution.name == 'info.json':
			continue

		num = solution.name.split('.')[0]
		problem = info[num]['problem']

		if problem not in result:
			result[problem] = solution.name
			continue

		if is_latest(solution.name, result[problem]):
			result[problem] = solution.name

	return result


def main():
	global info, solution_dir

	try:
		solution_dir = sys.argv[1]
	except IndexError:
		sys.exit('ERROR: Please specify the path to your solutions') 

	solutions = []
	try:
		solutions = os.scandir(solution_dir)
	except FileNotFoundError:
		sys.exit('ERROR: That directory does not exist')

	try:
		info_file = open(f'{solution_dir}/info.json')
		info = json.load(info_file)
		info_file.close()
	except FileNotFoundError:
		sys.exit('ERROR: The info.json file does not exist in that directory')
			
	solutions = keep_most_recent(solutions)
	
	total = len(info)
	unique = len(solutions)
	print(f'INFO: Ignoring {total - unique} solutions that have newer versions')

	if not os.path.exists('result'):
		os.mkdir('result')
		print(f'INFO: Created result folder')

	done = 0
	for problem, file in solutions.items():
		process(problem, file)
		done += 1
		print(f'INFO: Done {done}/{unique}')
		time.sleep(60 / API_CALLS_PER_MIN)


if __name__ == '__main__':
	main()
