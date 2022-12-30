#!/bin/bash

export WINEPREFIX="$HOME/software/wine/build_mclient"
product="mclientqt"
python="$WINEPREFIX/drive_c/Python"
pyinstaller="$python/Scripts/pyinstaller.exe"
binariesdir="$HOME/binaries"
srcdir="$HOME/bin/$product/src"
resdir="$HOME/bin/$product/resources"
cmd="$HOME/bin/$product/build/Wine/$product.cmd"
shareddir="$HOME/bin/skl_shared_qt"
tmpdir="$WINEPREFIX/drive_c/$product" # Will be deleted!
# Will be deleted! Should not be empty, root may be damaged otherwise
sharedtmp="$WINEPREFIX/drive_c/skl_shared_qt"
builddir="$tmpdir/$product" # Will be deleted!

if [ ! -e "$pyinstaller" ]; then
    echo "pyinstaller is not installed!"; exit
fi

if [ ! -e "$cmd" ]; then
    echo "File $cmd does not exist!"; exit
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
cp -r "$shareddir"/src/* "$sharedtmp"/src/
cp -r "$shareddir"/resources/* "$sharedtmp"/resources/
cp -r "$srcdir"/* "$tmpdir"
cp -r "$resdir" "$builddir"
cp "$cmd" "$builddir"
cd "$tmpdir"
# Icon path should be windows-compliant
wine "$pyinstaller" -w -i ./$product/resources/$product.png "$product.py"
mv "$tmpdir/dist/$product"/* "$builddir/app"
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
