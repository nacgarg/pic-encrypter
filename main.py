from PIL import Image
from encrypter import Encrypter
import argparse
import os
import random

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
	im = Image.open("images/"+str(random.randint(0, 5))+".jpg")
	pix = im.load()

	encrypted, pwd = crypt.encrypt(args.message, 10)
	x=0
	counter = 0
	if (len(encrypted) % 3 == 0):
		encrypted+="\x00"
	while (x < len(encrypted)):
		r = ord(encrypted[x])
		if (x+1 >= len(encrypted)):
			g = 0
		else: 
			g = ord(encrypted[x+1])
		if (x+2 >= len(encrypted)):
			b = 0
		else: 
			b = ord(encrypted[x+2])
		print (r, g, b)
		pix[0, counter] = (r, g, b)
		x+=3
		counter += 1
	im.save(args.image)
	print "Here's your password for decryption" + pwd
#	with open(args.image, "a") as f:
#		f.write("\n" + pwd)

def decrypt():
	with open(args.image) as fh:
		for line in fh:
			pass
		last = line
	pwd = args.password
	im = Image.open(args.image)
	pix = im.load()
	encrypted = ""
	i = 0
	notdone = True
	while notdone:
		for x in range(0, 3):
			if (pix[0, i][x] != 0):
				encrypted += chr(pix[0, i][x])
			else:
				notdone = False
		i+=1
	print "Done! Here's the message:\n" + crypt.decrypt(encrypted, pwd)

if (args.message == "check_string_for_empty"):
	print "You did not specify a message, so I am going to decrypt."
	decrypt()
else:
	print "Encrypting " + args.message + "..."
	encrypt()
