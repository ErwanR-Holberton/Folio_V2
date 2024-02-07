#!/usr/bin/env python3
import sys
x = int(sys.argv[1])
tile_size = 32
for offset in range(100, -10, -1):
    if offset < 0:
        var = int((x -(offset - 32))/tile_size)
    else:
        var = int((x - offset)/tile_size)
    print (offset, var)
