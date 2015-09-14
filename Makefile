install:
	rm -rf ./bin
	mkdir bin
	cat encrypter.py main.py > ./bin/pic-encrypt
	chmod 777 bin/pic-encrypt
	sudo cp `pwd`/bin/pic-encrypt /usr/local/bin/pic-encrypt
	sudo cp -r `pwd`/pic-encrypt-images/ /usr/local/bin/pic-encrypt-images
	echo "Done. You can now run pic-encrypt from the command line."

all: install