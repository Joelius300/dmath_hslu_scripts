To create .tns files for the TI (with zsh) use:

autoload zmv
zmv '(*.py)' '$1.tns'


To reverse it use:

zmv '(*.py).tns' '$1'


Or in bash (e.g. git bash for windows):

for f in *.py; do mv -- "$f" "$f.tns"; done

To reverse it:

for f in *.tns; do mv -- "$f" "${f%.tns}"; done
