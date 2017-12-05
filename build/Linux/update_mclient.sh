#!/bin/sh

#mkdir ./mclient

./update_here.sh
./build.sh
mkdir -p ./mclient/tkhtml/Linux
mv ./build/exe.linux-i686-3.4/* mclient
rmdir ./build/exe.linux-i686-3.4
rmdir ./build
cp -ru dics locale resources mclient.cfg mclient/
cp -rv /usr/lib/python3.4/site-packages/tkinterhtml/tkhtml/Linux/* ./mclient/tkhtml/Linux/
./clean_up.sh
