#!/bin/sh

./update_here.sh
./build.sh
cp $HOME/tmp/ars/windows.7z .
7z x windows.7z
rm windows.7z
cp -ru build/exe.win32-3.4/* mclient/
cp -ru dics locale resources mclient.cfg mclient/
cd mclient && wine mclient.exe
cd .. && 7z a windows.7z mclient/ && rm -r build mclient
./clean_up.sh
