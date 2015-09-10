install:
	rm -rf ./bin
	mkdir bin
	cat encrypter.py main.py > ./bin/pic-encrypt
	chmod 777 bin/pic-encrypt
	sudo ln -s `pwd`/bin/pic-encrypt /usr/local/bin/pic-encrypt
	echo "Done. You can now run pic-encrypt from the command line."

all: install