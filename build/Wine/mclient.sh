#!/bin/bash

export WINEPREFIX="$HOME/base/software/wine/python38_vista"
product="mclient"
python="$WINEPREFIX/drive_c/Python"
pyinstaller="$python/Scripts/pyinstaller.exe"
binariesdir="$HOME/binaries"
srcdir="$HOME/bin/$product/src"
resdir="$HOME/bin/$product/resources"
cmd="$HOME/bin/$product/build/Wine/$product.cmd"
tkhtmldir="$python/Lib/site-packages/tkinterhtml/tkhtml/Windows"
shareddir="$HOME/bin/skl_shared"
tmpdir="$WINEPREFIX/drive_c/$product" # Will be deleted!
# Will be deleted! Should not be empty, root may be damaged otherwise
sharedtmp="$WINEPREFIX/drive_c/skl_shared"
builddir="$tmpdir/$product" # Will be deleted!

if [ ! -e "$pyinstaller" ]; then
    echo "pyinstaller is not installed!"; exit
fi

if [ ! -e "$cmd" ]; then
    echo "File $cmd does not exist!"; exit
fi

if [ ! -d "$tkhtmldir" ]; then
    echo "Folder $tkhtmldir does not exist!"; exit
fi

if [ ! -d "$binariesdir/$product" ]; then
    echo "Folder $binariesdir/$product does not exist!"; exit
fi

if [ ! -d "$srcdir" ]; then
    echo "Folder $srcdir does not exist!"; exit
fi

if [ ! -d "$resdir" ]; then
    echo "Folder $resdir does not exist!"; exit
fi

if [ ! -d "$shareddir/src" ]; then
    echo "Folder $shareddir/src does not exist!"; exit
fi

if [ ! -d "$shareddir/resources" ]; then
    echo "Folder $shareddir/resources does not exist!"; exit
fi

# Build with pyinstaller
rm -rf "$tmpdir"
rm -rf "$sharedtmp"/*
mkdir -p "$sharedtmp"/{src,resources}
mkdir -p "$builddir/app/tkinterhtml/tkhtml"
cp -r "$shareddir"/src/* "$sharedtmp"/src/
cp -r "$shareddir"/resources/* "$sharedtmp"/resources/
cp -r "$srcdir"/* "$tmpdir"
cp -r "$resdir" "$builddir"
cp "$cmd" "$builddir"
cd "$tmpdir"
# Icon path should be windows-compliant
wine "$pyinstaller" -w -i ./$product/resources/icon_64x64_$product.ico "$product.py"
mv "$tmpdir/dist/$product"/* "$builddir/app"
cp -r "$tkhtmldir" "$builddir/app/tkinterhtml/tkhtml/"
# Tesh launch
cd "$builddir/app"
wine ./$product.exe&
# Update the archive
read -p "Update the archive? Y/n" choice
if [ "$choice" = "N" ] || [ "$choice" = "n" ]; then
    exit;
fi
rm -f "$binariesdir/$product/windows.7z"
7z a "$binariesdir/$product/windows.7z" "$builddir"
rm -rf "$tmpdir"
