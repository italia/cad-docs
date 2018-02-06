#!/bin/bash

mkdir rst
for ii in $( ls input/); do
  name=${ii%%.*}
  python3 normattiva2rst.py input/"$ii" > rst/"$name".rst
done
