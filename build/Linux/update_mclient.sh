#!/bin/sh

#mkdir ./mclient

./update_here.sh
./build.sh
mkdir ./mclient
mv ./build/exe.linux-i686-3.4/* mclient
rmdir ./build/exe.linux-i686-3.4
rmdir ./build
cp -ru dics locale resources mclient.cfg mclient/
cp -rv ./mclient_bin_extra/* ./mclient/
./pack.sh
rm -rf ./mclient
./clean_up.sh
