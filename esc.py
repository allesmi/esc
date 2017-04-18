#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import io, sys
import random

def get_rules(f):
	rules = []
	category = ""
	for line in f:
			line = line.strip()
			if not line:
				continue
			first_char = line[0]
			if first_char.isnumeric():
				category = line[3:]
			elif first_char in "-+":
				line = line[2:]
				rules.append("{}: {}".format(category, line))
	return rules

def get_countries():
	return ['Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'France', 'Georgia', 'Germany', 'Hungary', 'Israel', 'Italy', 'Latvia', 'Lithuania', 'Malta', 'Poland', 'Russia', 'Serbia', 'Spain', 'Sweden', 'The Netherlands', 'Ukraine', 'United Kingdom'];

def export(pairs, file,  fmt='tsv'):	
	fmt_string = export.fmt_strings.get(fmt, None)

	if not fmt_string:
		return

	for p in pairs:
		country, rule = p

		file.write(fmt_string.format(country, rule))
export.fmt_strings = { 
	'tsv': '{}\t{}\n',
	'csv': '{};{}\n'
}

def main(rules_file):
	with io.open(rules_file, 'r', encoding='utf8') as f:
		rules = get_rules(f)

	if not rules:
		print("No rules found in '{}'!".format(rules_file))
		return -1

	countries = get_countries()

	# Reporting
	print("Read {} rules from '{}'.".format(len(rules), rules_file))
	print("Got {} countries.".format(len(countries)))

	# The Great Shuffling
	random.shuffle(rules)
	random.shuffle(countries)

	pairs = zip(countries, rules)

	export(pairs, sys.stdout, fmt='tsv')

	return 0

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Aids an ESC drinking game raffle.')
	parser.add_argument('file', help='File containing rules', nargs='?', default='esc_trim.mdown')
	args = parser.parse_args()

	sys.exit(main(args.file))