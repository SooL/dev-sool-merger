# dev-sool-merger
Merge tool to regenerate final files

## Basic use

 - Using `dev-sool-builder` from https://github.com/SooL/dev-sool-builder , generate a set of structural headers The output directory is `out`.
 - Copy the generated headers to a temp directory `temp`.
 - Add the header files from https://github.com/SooL/core-basefiles to `temp`. 
 - Run `python3 dev-sool-merger/sool_merger.py -s temp/ -m out/include -f "*_struct.h"` 

