#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import random
import sys
from copy import copy
from binascii import hexlify, unhexlify
import pickle

def parse_arguments():
	parser = argparse.ArgumentParser(description="Xander's magic encryptificationifier")
	parser.add_argument("infile", metavar="I", type=str, help="Input file")
	parser.add_argument("outfile", metavar="O", type=str, help="Output file")
	return parser.parse_args()

def doTuring(data, iters):
	tape = copy(data)
	place = random.randint(0, len(tape) - 1)
	state = '1'
	for i in range(iters):
		if state == '1' and tape[place] == '1':
			tape[place] = '0'
			place += 1
		elif state == '1'and tape[place] == '0':
			tape[place] = '1'
			place += 1
			state = '0'
		elif state == '0' and tape[place] == '1':
			state = '1'
			place += 1
		elif state == '0' and tape[place] == '0':
			place += 1
		if place >= len(tape):
			place -= len(tape)
		if place <= -1:
			place += len(tape)
		print('.'.rjust((60 * i) / iters))
		sys.stdout.write("\033[F")
	tape = ''.join(tape)
	nData = [tape[i:i+7].zfill(8) for i in range(0, len(tape), 7)]
	return [nData, place, state]

def encrypt(string, pwd):
	info = ''
	for char in string:
		info += bin(int(hexlify(char), 16))[2:].zfill(7)
	info = list(info)
	rslt = doTuring(info, pwd)
	eInfo = rslt[0]
	code = [hex(pwd * 3)[2:], '.', hex(rslt[1] * 7)[2:], '.', rslt[2]]
	code = ''.join(code)
	print("Passcode for decryption:")
	print(code)
	for i in range(len(eInfo)):
		eInfo[i] = unhexlify(hex(int(eInfo[i], 2))[2:].zfill(2))
	return ''.join(eInfo)

def main():
	args = parse_arguments()
	contents = open(args.infile).read()
	data = list(contents)
	print "len(data): ", len(data)
	n = random.randint(10 * len(data), (len(data) * 40) + 200000)
	enc = encrypt(data, n)
	pickle.dump(enc, open(args.outfile, 'wb'))

print("Welcome to the encryption system Mk. 2!")
if __name__ == '__main__':
	main()