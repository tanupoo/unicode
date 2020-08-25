unicode
=======

a unicode tool.  The features are below for example.

- list categories.
- code points.
- showing charactors.
- normalizing.
- etc.

## example

```
unicode list
unicode list -c scripts
unicode list -c scripts -v
unicode list -c scripts -a
unicode list -k rokee
unicode list -c scripts -k rokee
unicode list -c 'East Asian Scripts' -k 'CJK Extension C'

unicode read -f sample/nfd.txt
unicode read -f sample/nfd.txt -n NFC -o output.txt
unicode read -f sample/nfd.txt -n NFD -l
cat sample/nfd.txt | ./unicode.py read

unicode show -N 1F64b 1f3fb
unicode show 1F64b 1f3fb
unicode show 845B e0100
unicode show 0066 200D 0066 200D 0074
unicode show FB50 FB62 -s
unicode show 3041 304F -s -l -N
unicode show 3041 304F -s -l -N -v
unicode show 12353 12367 -s -i 
```

