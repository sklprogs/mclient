#!/bin/bash

ver='3.5'

./update_here.sh
./build.sh
mkdir -p ./mclient/app
mv ./build/exe.linux-i686-$ver/* ./mclient/app/
rmdir -p build/exe.linux-i686-$ver
cp -ru ./resources ./mclient/
rm -r ./mclient/app/{libicudata.so.54,libicui18n.so.54,libicuuc.so.54,libQt*,platforms,imageformats}
rm -r ./mclient/app/lib/python$ver/{dawg_python,enchant,importlib,lib2to3,PIL,pydoc_data,PyQt*,pymorphy2*}
rm -r ./mclient/app/lib/python$ver/tkinterhtml/tkhtml/{MacOSX,Windows}
./pack.sh
rm -rf ./mclient
./clean_up.sh
