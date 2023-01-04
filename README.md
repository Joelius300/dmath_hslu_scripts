## DMATH Python Scripts HSLU

Micropython 2014 scripts for DMATH, designed for the (black) TI-Nspire™ CX CAS I (not tested on the (red) successor II).

### Rename all to .tns

To create .tns files for the TI (with zsh) use:

```bash
autoload zmv
zmv '(*.py)' '$1.tns'
```

To reverse it use:

```bash
zmv '(*.py).tns' '$1'
```

Or in bash (e.g. git bash for windows):

```bash
for f in *.py; do mv -- "$f" "$f.tns"; done
```

To reverse it:

```bash
for f in *.tns; do mv -- "$f" "${f%.tns}"; done
```

### Disclaimer

Use at your own risk; it may not be allowed anymore or contain errors. Even though it's public now, this was just hacked together for personal use in one semester and if you expect more, you'll be disappointed.

License: MIT
