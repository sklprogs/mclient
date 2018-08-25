#!/bin/sh

./update_here.sh
./build.sh
mkdir -p ./mclient/app/tkhtml
mv ./build/exe.win32-3.4/* ./mclient/app/
rmdir -p build/exe.win32-3.4
cp -r /usr/local/bin/shared_bin_win/* ./mclient/app/
cp -r /usr/lib/python3.4/site-packages/tkinterhtml/tkhtml/Windows/ ./mclient/app/tkhtml/
cp -r ./resources ./user ./mclient/
cp ./mclient.cmd ./mclient/
rm -r ./mclient/app/PIL*

cd mclient/app && wine mclient.exe
read -p "Update the archive? (y/n) " choice
if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
	mv -fv $HOME/binaries/mclient/windows.7z $HOME/binaries/mclient/windows\ \(OLD\).7z
	cd ../.. && 7z a $HOME/binaries/mclient/windows.7z mclient/ && rm -r mclient
	./clean_up.sh
fi
