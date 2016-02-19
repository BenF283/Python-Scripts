# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/ben/.spyder2/.temp.py
"""

import sys

def main(argv):
    

    for x in range(1, len(sys.argv)):

        numtofac = int(sys.argv[x])
        ans = numtofac
        for y in range(1, int(sys.argv[x])):
            numtofac = numtofac - 1   
            ans = ans * numtofac
        print ans
    
if __name__ == "__main__":
    main(sys.argv[1:])