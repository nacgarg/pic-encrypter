#! /usr/bin/python

import random
import copy
from binascii import hexlify
from binascii import unhexlify
from string import letters

def doTuring(data, iters):
	tape = copy.copy(data)
	place = random.randint(0,6)
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
		if place >= 7:
			place += -7
		if place <= -1:
			place += 7
	return ''.join([ '0', ''.join(str(x) for x in tape), '0', str(random.randint(0, 1)), '1', bin(place * 2)[2:].zfill(4), state])

def encrypt(info, pwd):
	info = info[2:].zfill(7)
	info = list(info)
	encinfo = doTuring(info, pwd)
	return ''.join(encinfo)

def dealWithData():
	encrypted = []
	path = input("Please give the filepath of the plain text file to be encrypted \n")
	text = open(path)
	data = list(text.read())
	data.pop()
	print(data)

	n = random.randint(1, 200000)
	print("Here is your password for the unencryption: ")
	pswrd = [ str(random.randint(0, 9)), random.choice(letters), str(random.randint(0, 9)), random.choice(letters)]
	pswrd = ''.join(pswrd)
	pswrd += hex(7 * n)[2:].zfill(6)
	print(pswrd)

	enc = ''
	enc2 = ''
	for i in range(len(data)):
		char = bin(int(hexlify(data[i]), 16))
		enc2 = encrypt(char, n)
		enc = unhexlify(hex(int(enc2, 2))[2:].zfill(4))
		encrypted.append(enc)
	encrypted = ''.join(encrypted)
	print(encrypted)
	pathTwo = input("Please give the filepath of the plain text file to be written to \n")
	text = open(pathTwo, 'w')
	text.write(encrypted)

print("Welcome to the encrypter!")
dealWithData()