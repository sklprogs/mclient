#!/bin/bash
# Do 'pip3 uninstall enum34' in case of receiving
# AttributeError: module 'enum' has no attribute 'IntFlag'

product="mclient"
productlow='mclient'
arch="x86_64"
os="Linux" # Linux or Wine
oslow="linux"
# We need to use Debian 10 or newer since Debian 9 has Python 3.5 by default 
# which is buggy (some blocks are skipped in EN-RU, "hello" article)
glibc="2.36"
pythonve="$HOME/software/python/3.11.2_mclient"
xlibdir="$pythonve/lib/python3.11/site-packages/Xlib"
schemas="$pythonve/lib/python3.11/site-packages/jsonschema_specifications/schemas"
binariesdir="$HOME/binaries"
appimagedir="$binariesdir/appimage"
srcdir="$HOME/bin/$product/src"
resdir="$HOME/bin/$product/resources"
tmpdir="/tmp/$product"   # Will be deleted!
builddir="$tmpdir/build" # Will be deleted!

export "ARCH=$arch"

source "$pythonve/bin/activate"

if [ "`which pyinstaller`" = "" ]; then
    echo "pyinstaller is not installed!"; exit
fi

if [ ! -d "$binariesdir/$product" ]; then
    echo "Folder $binariesdir/$product does not exist!"; exit
fi

if [ ! -d "$appimagedir" ]; then
    echo "Folder $appimagedir does not exist!"; exit
fi

if [ ! -d "$srcdir/keylistener" ]; then
    echo "Folder $srcdir/keylistener does not exist!"; exit
fi

if [ ! -d "$xlibdir" ]; then
    echo "Folder $xlibdir does not exist!"; exit
fi

if [ ! -d "$schemas" ]; then
    echo "Folder $schemas does not exist!"; exit
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
mkdir -p "$builddir" "$tmpdir/app/usr/bin" "$tmpdir/app/resources"
cp -r "$srcdir"/* "$builddir"
cp -r "$resdir" "$tmpdir/app/usr/bin/"
# For some reason, the built program cannot find locales
cp -r "$resdir/locale" "$tmpdir/app/resources/"
# For some reason, pyinstaller cannot find these modules
cp -r "$srcdir/keylistener" "$xlibdir" "$tmpdir/app/usr/bin/"
cd "$builddir"
pyinstaller "$product.py"
# Create AppImage
mv "$builddir/dist/$product"/* "$tmpdir/app/usr/bin/"
cp "$appimagedir/AppRun-$arch" "$tmpdir/app/AppRun"
cp "$appimagedir/appimagetool-$arch.AppImage" "$tmpdir"
cp "$HOME/bin/$product/build/$os/$product.desktop" "$tmpdir/app"
cp "$HOME/bin/$product/build/$os/$product.png" "$tmpdir/app"
mkdir "$tmpdir/app/usr/bin/jsonschema_specifications"
rsync -ar "$schemas/" "$tmpdir/app/usr/bin/jsonschema_specifications/schemas"
cd "$tmpdir"
# This argument allows to avoid a permission error
./appimagetool-$arch.AppImage --appimage-extract-and-run app
#read -p "Update the AppImage? (Y/n) " choice
#if [ "$choice" = "N" ] || [ "$choice" = "n" ]; then
#    exit;
#fi

mv -fv "$tmpdir/$productlow-$arch.AppImage" "$HOME/binaries/$product/$productlow-$oslow-$arch-glibc$glibc.AppImage"
rm -rf "$tmpdir"

deactivate
