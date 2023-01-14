#!/bin/bash

export WINEPREFIX="$HOME/software/wine/build_mclient"
python="$WINEPREFIX/drive_c/Python"
pyinstaller="$python/Scripts/pyinstaller.exe"
product="mclientqt"
shared="skl_shared_qt"
binariesdir="$HOME/binaries"
bindir="$HOME/bin"
productdir="$bindir/$product"
resdir="$bindir/$product/resources"
shareddir="$bindir/$shared"
cmd="$productdir/build/Wine/$product.cmd"
producttmp="$WINEPREFIX/drive_c/$product" # Will be deleted!
sharedtmp="$WINEPREFIX/drive_c/$shared"   # Will be deleted!
buildtmp="$producttmp/$product"           # Will be deleted!

if [ ! -e "$pyinstaller" ]; then
    echo "pyinstaller is not installed!"; exit
fi

if [ ! -e "$cmd" ]; then
    echo "File $cmd does not exist!"; exit
fi

if [ ! -d "$binariesdir/$product" ]; then
    echo "Folder $binariesdir/$product does not exist!"; exit
fi

if [ ! -d "$productdir" ]; then
    echo "Folder $productdir does not exist!"; exit
fi

if [ ! -d "$resdir" ]; then
    echo "Folder $resdir does not exist!"; exit
fi

if [ ! -d "$shareddir" ]; then
    echo "Folder $shareddir does not exist!"; exit
fi

rsync -aL --delete-before --exclude='.git' "$productdir/" "$producttmp"
rsync -aL --delete-before --exclude='.git' "$shareddir/" "$sharedtmp"

mkdir "$buildtmp"

cd "$producttmp"/src
# Icon path should be Windows-compliant. Only ICO and EXE formats are supported.
wine "$pyinstaller" -w -i ../resources/$product.ico "$product.py"

mv "$producttmp/src/dist/$product" "$buildtmp/app"
cp -r "$resdir" "$buildtmp"/
cp "$cmd" "$buildtmp"

# Tesh launch
cd "$buildtmp/app"
wine ./$product.exe&

# Update the archive
read -p "Update the archive? Y/n" choice
if [ "$choice" = "N" ] || [ "$choice" = "n" ]; then
    exit;
fi
rm -f "$binariesdir/$product/$product.7z"
7z a "$binariesdir/$product/$product.7z" "$buildtmp"
