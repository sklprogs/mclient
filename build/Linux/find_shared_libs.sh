find /bin -type f -perm /a+x -exec ldd {} \; | grep so | sed -e '/^[^\t]/ d' | sed -e 's/\t//' | sed -e 's/.*=..//' | sed -e 's/ (0.*)//' | sort | uniq -c | sort -n
