#!/bin/sh

./update_here.sh
./build.sh
mkdir -p ./mclient/app
mv ./build/exe.linux-i686-3.4/* ./mclient/app/
rmdir -p build/exe.linux-i686-3.4
cp -ru ./resources ./user ./mclient/
rm -r ./mclient/app/{libicudata.so.54,libicui18n.so.54,libicuuc.so.54,libQt*,platforms,imageformats}
rm -r ./mclient/app/lib/python3.4/{dawg_python,enchant,importlib,lib2to3,PIL,pydoc_data,PyQt*,pymorphy2*}
./pack.sh
rm -rf ./mclient
./clean_up.sh
