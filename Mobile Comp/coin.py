# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 03:54:56 2016

@author: ben
"""
import sys

def main(argv):
    #split message
    coins = sys.argv[1]
    coins = coins.split(',')
    splitcoin = coins[len(coins)-1].split(':')
    coins[len(coins)-1] = splitcoin[0]
    change = int(splitcoin[1])
    
    coincount = [0] * len(coins)
    
    #Calculate coins reqiored
    while (change > 0):
        for x in range(0,len(coins)):
            if(change - int(coins[x]) >= 0):
                change = change - int(coins[x])
                coincount[x] = coincount[x] +1
                break
                
     #Print coin output
    for x in range(0,len(coins)):
        print coincount[x], 'x', coins[x]
    
    

    
    
if __name__ == "__main__":
    main(sys.argv[1:])