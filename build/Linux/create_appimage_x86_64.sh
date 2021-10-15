#!/bin/bash

product="mclient"
productlow="mclient"
arch="x86_64"
os="Linux" # Linux or Wine
oslow="linux"
# We need to use Debian 10 or newer since Debian 9 has Python 3.5
# by default which is buggy (some blocks are skipped in EN-RU, "hello"
# article)
glibc="2.31"
binariesdir="$HOME/binaries"
appimagedir="$binariesdir/appimage"
srcdir="$HOME/bin/$product/src"
resdir="$HOME/bin/$product/resources"
# /usr/local/lib/python3.9/dist-packages in case of using sudo pip3
tkhtmldir="$HOME/.local/lib/python3.9/site-packages/tkinterhtml/tkhtml/Linux"
tmpdir="/tmp/$product"   # Will be deleted!
builddir="$tmpdir/build" # Will be deleted!

export "ARCH=$arch"

if [ "`which pyinstaller`" = "" ]; then
    echo "pyinstaller is not installed!"; exit
fi

if [ ! -d "$tkhtmldir" ]; then
    echo "Folder $tkhtmldir does not exist!"; exit
fi

if [ ! -d "$binariesdir/$product" ]; then
    echo "Folder $binariesdir/$product does not exist!"; exit
fi

if [ ! -d "$appimagedir" ]; then
    echo "Folder $appimagedir does not exist!"; exit
fi

if [ ! -d "$srcdir" ]; then
    echo "Folder $srcdir does not exist!"; exit
fi

if [ ! -d "$resdir" ]; then
    echo "Folder $resdir does not exist!"; exit
fi

if [ ! -e "$appimagedir/AppRun-$arch" ]; then
    echo "File $appimagedir/AppRun-$arch does not exist!"; exit
fi

if [ ! -e "$appimagedir/appimagetool-$arch.AppImage" ]; then
    echo "File $appimagedir/appimagetool-$arch.AppImage does not exist!"; exit
fi

if [ ! -e "$HOME/bin/$product/build/$os/$product.desktop" ]; then
    echo "File $HOME/bin/$product/build/$os/$product.desktop does not exist!"; exit
fi

if [ ! -e "$HOME/bin/$product/build/$os/$product.png" ]; then
    echo "File $HOME/bin/$product/build/$os/$product.png does not exist!"; exit
fi

# Build with pyinstaller
rm -rf "$tmpdir"
mkdir -p "$builddir" "$tmpdir/app/usr/bin/tkinterhtml/tkhtml" "$tmpdir/app/resources"
cp -r "$srcdir"/* "$builddir"
cp -r "$resdir" "$tmpdir/app/usr"
cp -r "$resdir/locale" "$tmpdir/app/resources/"
cd "$builddir"
pyinstaller "$product.py"
# Create AppImage
mv "$builddir/dist/$product"/* "$tmpdir/app/usr/bin"
cp -r "$tkhtmldir" "$tmpdir/app/usr/bin/tkinterhtml/tkhtml/"
cd "$tmpdir/app"
cp "$appimagedir/AppRun-$arch" "$tmpdir/app/AppRun"
cp "$appimagedir/appimagetool-$arch.AppImage" "$tmpdir"
cp "$HOME/bin/$product/build/$os/$product.desktop" "$tmpdir/app"
cp "$HOME/bin/$product/build/$os/$product.png" "$tmpdir/app"
cd "$tmpdir"
./appimagetool-$arch.AppImage app
read -p "Update the AppImage? (Y/n) " choice
if [ "$choice" = "N" ] || [ "$choice" = "n" ]; then
    exit;
fi
mv -fv "$tmpdir/$productlow-$arch.AppImage" "$HOME/binaries/$product/$productlow-$oslow-$arch-glibc$glibc.AppImage"
rm -rf "$tmpdir"
