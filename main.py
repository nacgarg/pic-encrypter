#!/usr/bin/env python

from PIL import Image
try:
    from encrypter import Encrypter
except ImportError:
    pass
import argparse
import os
from random import seed, randint

def valid_file(param):
    base, ext = os.path.splitext(param)
    if ext.lower() not in ('.bmp'):
        raise argparse.ArgumentTypeError('File must have a bmp extension')
    return param

parser = argparse.ArgumentParser(description='Encrypt and decrypt messages and hide them in an image.')
parser.add_argument('-i', dest="image", type=valid_file, metavar="image", help='Location of image you wish to decrypt or encrypt to.', required=True)
parser.add_argument('-m', dest="message", metavar="message", help='Message you want to encrypt.', default="check_string_for_empty")
parser.add_argument('-p', dest="password", metavar="password", help='Password (for decryption)')
args = parser.parse_args()
crypt = Encrypter()

def encrypt():
#	im = Image.open("telescope.jpg")
	im = Image.open("/usr/local/bin/pic-encrypt-images/"+str(randint(0, 5))+".jpg")
	pix = im.load()
	numArray = []

	if os.path.isfile(args.message):
		msg = open(args.message).read()
	else:
		msg = args.message
	iters = randint(len(msg) * 3, (len(msg) * 3) + 1000000)
#	print iters
	encrypted, pwd = crypt.encrypt(msg, iters)

	x=0
	sed = ''.join(pwd.split('.'))
	seed(sed)
	if (len(encrypted) % 3 == 0):
		encrypted+=chr(0)
		encrypted+=chr(0)
		encrypted+=chr(0)
	todo = len(encrypted) / 3.0
	bigness = im.size[0] * im.size[1]
	eRuns = (1.0/(1 - (1.0/bigness))) * (todo/2.0) * todo
	print "Estimated time for steganography: " + str(eRuns * (1.95e-06)) + "s"
	while (x < len(encrypted)):
		r = ord(encrypted[x])
		if (x+1 >= len(encrypted)):
#			print "zero"
			g = 0
		else: 
			g = ord(encrypted[x+1])
		if (x+2 >= len(encrypted)):
#			print "zero"
			b = 0
		else: 
			b = ord(encrypted[x+2]) 
		i, y = randint(0, im.size[0]-1), randint(0, im.size[1]-1)
		while (i, y) in numArray:
			i = randint(0, im.size[0]-1)
			y = randint(0, im.size[1]-1)
		numArray.append((i, y))
		pix[i, y] = (r, g, b)
		x+=3
	im.save(args.image)
	print "Here's your password for decryption " + pwd
#	with open(args.image, "a") as f:
#		f.write("\n" + pwd)

def decrypt():
	pwd = args.password
	sed = ''.join(pwd.split('.'))
	numArray = []
	seed(sed)
	im = Image.open(args.image)
	pix = im.load()
	encrypted = ""
	notdone = True
	while notdone:
		x, y = randint(0, im.size[0]-1), randint(0, im.size[1]-1)
		while (x, y) in numArray:
			x = randint(0, im.size[0]-1)
			y = randint(0, im.size[1]-1)
		numArray.append((x, y))
		for i in range(0, 3):
			if (pix[x, y][i] != 0):
				encrypted += chr(pix[x, y][i])
			else:
				notdone = False
	print "Done! Here's the message:\n" + crypt.decrypt(encrypted, pwd)

if (args.message == "check_string_for_empty"):
	print "You did not specify a message, so I am going to decrypt."
	decrypt()
else:
	print "Encrypting " + args.message + "..."
	encrypt()
