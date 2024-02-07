#!/usr/bin/env python3
import sys
x = int(sys.argv[1])
tile_size = 32
for y in range(40, -10, -1):
    if y < 10 and y >= 0:
        print (end=" ")
    print (y, end=" ")
print()
for x in range(-5, 5):
    for offset in range(40, -10, -1):
        if offset < 0:
            var = int((x -(offset - 32))/tile_size)
        else:
            var = int((x - offset)/tile_size)
        if var < 10 and var >= 0:
            print (end=" ")
        print (var, end=" ")
    print ()
