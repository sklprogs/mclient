#!/bin/sh

./update_here.sh
./wine_build.sh
cp $HOME/tmp/ars/windows.7z .
7z x windows.7z
rm windows.7z
cp -rvu build/exe.win32-3.4/* mclient/
cp -rvu dics locale resources mclient.cfg mclient/
cd mclient && wine mclient.exe
cd .. && 7z a windows.7z mclient/ && rm -r build mclient
