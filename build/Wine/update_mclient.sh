#!/bin/sh

./update_here.sh
./build.sh
cp $HOME/tmp/ars/windows.7z .
7z x windows.7z
rm windows.7z
cp -ru build/exe.win32-3.4/* mclient/
cp -ru dics locale resources mclient.cfg mclient/
cd mclient && wine mclient.exe
read -p "Update the archive?" choice
if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
	cd .. && 7z a windows.7z mclient/ && rm -r build mclient
	mv -fv $HOME/tmp/ars/windows.7z $HOME/tmp/ars/windows\ \(OLD\).7z
	mv -v ./windows.7z $HOME/tmp/ars/windows.7z
fi
./clean_up.sh
