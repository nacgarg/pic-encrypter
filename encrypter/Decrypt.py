#! /usr/bin/python
from copy import copy
from binascii import unhexlify, hexlify

def unTuring(d, itr, st, pl):
	tp = copy(d)
	for i in range(itr):
		pl -= 1
		if pl == -1:
			pl = 6
		if st == '1' and tp[pl] == '1':
			st = '0'
		elif st == '1' and tp[pl] == '0':
			tp[pl] = '1'
		elif st == '0' and tp[pl] == '1':
			st = '1'
			tp[pl] = '0'
	return ''.join(tp)

def decrypt(pwd, info):
	i_1 = list(info[1:8])
	i_3 = info[15]
	i_2 = (int(info[11:15], 2) / 2)
	n = unTuring(i_1, pwd, i_3, i_2).zfill(8)
	return unhexlify(hex(int(n, 2))[2:].zfill(2))

def dealWithData():
	msg = ''
	pth = input("Input filepath of plain text file to decrypt \n")
	txt = open(pth)
	txt = list(txt.read())
	code = input("Provide 10 character password (in quotes)\n")
	code = int(code[4:], 16) / 7
	txt_list = [txt[i:i+2] for i in range(0, len(txt), 2)]
	for z in range(len(txt_list)):
		txt_list[z] = ''.join(txt_list[z])
		txt_list[z] = bin(int(hexlify(txt_list[z]), 16))[2:].zfill(16)
		msg += decrypt(code, txt_list[z])
	print("Done!")
	print(msg)

print("Welcome to the unscrambler!")
dealWithData()