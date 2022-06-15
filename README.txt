To create .tns files for the TI use:

autoload zmv
zmv '(*.py)' '$1.tns'


To reverse it use:

zmv '(*.py).tns' '$1'
