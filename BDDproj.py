import unittest
from pyeda.inter import *
from functools import reduce

#evenList = [x for x in range(33) if (x%2 == 0)]
#primeList = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

#our graph 'G' with 32 nodes starting from 0 to 31
G = range(0,32)
#R is our edges 
R = [(i,j) for i in G for j in G if(i+3)%32 == j%32 or (i+7)%32 == j%32]

def EVEN(x:int)-> bool:
    return (x%2 == 0)
def PRIME(x:int)-> bool:
    return (x%2 == 1)



class TestGraph(unittest.TestCase):
    def testEVEN(self):
        self.assertEqual(EVEN(14),True)
        self.assertEqual(EVEN(13),False)
    def testODD(self):
        self.assertEqual(ODD())

def main():
    #R is our edges 
    R = [(i,j) for i in G for j in G if(i+3)%32 == j%32 or (i+7)%32 == j%32]
   
    #print(R, end = ' ')
    print(EVEN(14))

if __name__ == "__main__":
    unittest.main()