#!/bin/bash

product="mclient"
productlow="mclient"
arch="x86_64"
os="Linux" # Linux or Wine
oslow="linux"
# We need to use Debian 10 or newer since Debian 9 has Python 3.5
# by default which is buggy (some blocks are skipped in EN-RU, "hello"
# article)
glibc="2.36"
pythonve="$HOME/software/python/mclient_tk_3.11.2_x64"
binariesdir="$HOME/binaries"
appimagedir="$binariesdir/appimage"
srcdir="$HOME/sklprogs/$product/src"
resdir="$HOME/sklprogs/$product/resources"
tkhtmldir="$pythonve/lib/python3.11/site-packages/tkinterhtml/tkhtml/Linux/"
tmpdir="/tmp/$product"   # Will be deleted!
builddir="$tmpdir/build" # Will be deleted!

# Actions that may be required before building:
# sudo ln -s /usr/share/tcltk/tcl8.6/tcl8 /usr/share/tcltk/tcl8
# sudo ln -s /usr/share/tcltk/tk8.6 /usr/share/tcltk/tk8
# sudo ln -s $pythonve/lib/python3.11/site-packages/tkinterhtml/tkhtml/Linux/64-bit/Tkhtml /usr/share/tcltk/Tkhtml
# ln -s $HOME/bin/skl_shared/src $pythonve/lib/python3.11/site-packages/skl_shared
# ln -s $HOME/bin/skl_shared/resources $pythonve/lib/python3.11/site-packages/resources

export "ARCH=$arch"

source "$HOME/tmp/pythonve/bin/activate"

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

if [ ! -e "$HOME/sklprogs/$product/build/$os/$product.desktop" ]; then
    echo "File $HOME/sklprogs/$product/build/$os/$product.desktop does not exist!"; exit
fi

if [ ! -e "$HOME/sklprogs/$product/build/$os/$product.png" ]; then
    echo "File $HOME/sklprogs/$product/build/$os/$product.png does not exist!"; exit
fi

# Build with pyinstaller
rm -rf "$tmpdir"
mkdir -p "$builddir" "$tmpdir/app/usr/bin/tkinterhtml/tkhtml" "$tmpdir/app/resources"
cp -r "$srcdir"/* "$builddir"
cp -r "$resdir" "$tmpdir/app/usr/bin"
cp -r "$resdir/locale" "$tmpdir/app/resources/"
cd "$builddir"
pyinstaller "$product.py"
# Create AppImage
mv "$builddir/dist/$product"/* "$tmpdir/app/usr/bin"
cp -r "$tkhtmldir" "$tmpdir/app/usr/bin/tkinterhtml/tkhtml/"
cd "$tmpdir/app"
cp "$appimagedir/AppRun-$arch" "$tmpdir/app/AppRun"
cp "$appimagedir/appimagetool-$arch.AppImage" "$tmpdir"
cp "$HOME/sklprogs/$product/build/$os/$product.desktop" "$tmpdir/app"
cp "$HOME/sklprogs/$product/build/$os/$product.png" "$tmpdir/app"
cd "$tmpdir"
./appimagetool-$arch.AppImage app
read -p "Update the AppImage? (Y/n) " choice
if [ "$choice" = "N" ] || [ "$choice" = "n" ]; then
    exit;
fi
mv -fv "$tmpdir/$productlow-$arch.AppImage" "$HOME/binaries/$product/$productlow-$oslow-$arch-glibc$glibc.AppImage"
rm -rf "$tmpdir"
deactivate
