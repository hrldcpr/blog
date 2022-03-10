#!/usr/bin/env python3

import sys

for line in sys.stdin:
  print(line.replace('>T<', '>X<'))
