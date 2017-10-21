#!/bin/sh

#mkdir ./mclient

./update_here.sh
./build.sh
mv ./build/exe.linux-i686-3.4/* mclient
rmdir ./build/exe.linux-i686-3.4
rmdir ./build
cp -ru dics locale resources mclient.cfg mclient/
./clean_up.sh
