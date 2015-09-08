#! /usr/bin/python
import argparse
from binascii import hexlify, unhexlify
from copy import copy
import pickle
import sys
import time

def parse_arguments():
	parser = argparse.ArgumentParser(description="Xander's magic decryptifier.")
	parser.add_argument("infile", metavar="I", type=str, help="Input file")
	parser.add_argument("password", metavar="P", type=str, help="Password")
	return parser.parse_args()

def unTuring(t, st, pl, n):
	tp = copy(t)
	for x in range(n):
		pl -= 1
		if pl == -1:
			pl += len(tp)
		if st == '1' and tp[pl] == '1':
			st = '0'
		elif st == '1' and tp[pl] == '0':
			tp[pl] = '1'
		elif st == '0' and tp[pl] == '1':
			st = '1'
			tp[pl] = '0'
		print('.'.rjust((60 * x) / n))
		sys.stdout.write("\033[F")
	tp = ''.join(tp)
	return [tp[i:i+7].zfill(8) for i in range(0, len(tp), 7)]

def decrypt(pwd, string):
	pwd = pwd.split('.')
	iters = int(pwd[0], 16) / 3
	p = int(pwd[1], 16) / 7
	s = pwd[2]
	dat = ''
	for char in string:
		dat += bin(int(hexlify(char), 16))[2:].zfill(7)
	unEnc = unTuring(list(dat), s, p, iters)
	for i in range(len(unEnc)):
		unEnc[i] = unhexlify(hex(int(unEnc[i], 2))[2:].zfill(2))
	print("Done!")
	print ''.join(unEnc)

def main():
	args = parse_arguments()
	startTime = time.time()
	decrypt(args.password, pickle.load(open(args.infile, 'rb')))	
	print time.time() - startTime

if __name__ == "__main__":
	main()


