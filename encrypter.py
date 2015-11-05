#!/usr/bin/env python

from binascii import hexlify, unhexlify
from copy import copy
import random
import sys

class Encrypter():
	def __init__(self):
		pass

	def decrypt(self, string, pwd):
		print pwd
		pwd = pwd.split('.')
		iters = int(pwd[0], 16) / 3
		p = int(pwd[1], 16) / 7
		s = pwd[2]
		dat = ''
		for char in string:
			dat += bin(int(hexlify(char), 16))[2:].zfill(7)
		unEnc = self._unTuring(list(dat), s, p, iters)
		for i in range(len(unEnc)):
			unEnc[i] = unhexlify(hex(int(unEnc[i], 2))[2:].zfill(2))
		return ''.join(unEnc)

	def encrypt(self, string, pwd):
		print pwd
		info = ''
		for char in string:
			info += bin(int(hexlify(char), 16))[2:].zfill(7)
		info = list(info)
		rslt = self._doTuring(info, pwd)
		eInfo = rslt[0]
		code = [hex(pwd * 3)[2:], '.', hex(rslt[1] * 7)[2:], '.', rslt[2]]
		code = ''.join(code)
		for i in range(len(eInfo)):
			eInfo[i] = unhexlify(hex(int(eInfo[i], 2))[2:].zfill(2))
		return ''.join(eInfo), code #Returns encrypted, password

	def _doTuring(self, data, iters):
		print "Expected seconds for encryption: " + str(iters/144689)
		tape = copy(data)
		place = random.randint(0, len(tape) - 1)
		state = '1'
		for i in range(iters):
			if state == '1' and tape[place] == '1':
				tape[place] = '0'
			elif state == '1'and tape[place] == '0':
				tape[place] = '1'
				state = '0'
			else: 
				state = tape[place] # This is the new solution
#			elif state == '0' and tape[place] == '1':
#				state = '1'
#			elif state == '0' and tape[place] == '0':
				# Nothing here
			place += 1
			place -= len(tape) * (place == len(tape))
			print('.'.rjust((60 * i) / iters))
			sys.stdout.write("\033[F")
		tape = ''.join(tape)
#		print "from doTuring: " + str([len(tape), place, state])
		nData = [tape[i:i+7].zfill(8) for i in range(0, len(tape), 7)]
		return [nData, place, state]

	def _unTuring(self, t, st, pl, n):
		print "Expected seconds for decryption: " + str(n/144689)
		print n
		tp = copy(t)
		for x in range(n):
			pl -= 1
			pl += len(tp) * (pl == -1)
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