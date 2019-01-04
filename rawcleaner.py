#!/usr/local/bin/python3

from os import walk, remove, getcwd, path
from sys import argv, exit

DEFAULT_RAW_EXT = "nef"

ERR_NOT_DIR = "Error: path must be a directory"
ERR_USAGE = "Usage: ./rawcleaner.py [ -e ext ] [ -p path ] [ -f ]" \
			"\n\t-e\traw file extension; default: NEF" \
			"\n\t-p\tpath to scan; default: current working directory" \
			"\n\t-f\tremove without asking for confirmation" \
			"\n\te.g. ./rawcleaner.py -e cr2 -p ../photos -f"

COLOR_RED = '\033[91m'
COLOR_DEFAULT = '\033[39m'

def exit_error(error):
	print(error)
	exit(1)

def color_string(str, color):
	return '{}{}{}'.format(color, str, COLOR_DEFAULT)

value_args = dict()
value_args['-p'] = None
value_args['-e'] = None
flag_args = dict()
flag_args['-f'] = False

i = 1
while i < len(argv):
	if argv[i] in value_args:
		if i + 1 < len(argv):
			value_args[argv[i]] = argv[i+1]
			i = i + 2
		else:
			exit_error(ERR_USAGE)
	elif argv[i] in flag_args:
		flag_args[argv[i]] = True
		i = i + 1
	else:
		exit_error(ERR_USAGE)

if value_args['-p']:
	dir_path = value_args['-p']
else:
	dir_path = getcwd()

if value_args['-e']:
	raw_ext = value_args['-e']
	if raw_ext[0] == '.':
		raw_ext = raw_ext[1:]
else:
	raw_ext = DEFAULT_RAW_EXT

force = flag_args['-f']

filelist = []
for (dp, dn, fn) in walk(dir_path):
	filelist.extend(fn)

jpgs = set()
raws = set()

for file in filelist:
	if file[-4:].lower() == '.' + raw_ext:
		raws.add(file[0:-4])
	elif file[-4:].lower() == '.jpg':
		jpgs.add(file[0:-4])

raws_to_delete = raws.difference(jpgs)

print('JPEG files:\t{:4d}'.format(len(jpgs)))
print('{:s} files:\t{:4d}'.format(raw_ext.upper(), len(raws)))
if len(raws_to_delete) == 0:
	print('No {:s} files to remove'.format(raw_ext.upper()))
	exit()
else:
	print('Files to remove: {:4d}'.format(len(raws_to_delete)))
	for file in raws_to_delete:
		print(color_string('\t{}.{}'.format(file, raw_ext), COLOR_RED))

cont = None
while not force and not cont in ['', 'y', 'n']:
	cont = input('Continue? (y/N): ').lower()

if cont != 'y':
	exit(0)

for file in raws_to_delete:
	remove('{}.{}'.format(file, raw_ext))
