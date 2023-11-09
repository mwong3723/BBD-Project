import unittest
from pyeda.inter import *
from functools import reduce
from pyeda.boolalg.bdd import BinaryDecisionDiagram

#Most if not all of my commented out
#print() functions were used as debugger

#Global Variables
varX = [bddvar(f"{'x'*2}" + str(i)) for i in range(5)]
varY = [bddvar(f"{'y'*2}" + str(i)) for i in range(5)]

#Function used to initilze graph using a matrix
def initGraph()->list[list[bool]]:
    graphG = [[False]*32 for _ in range(32)]
    for i in range(0,31):
        for j in range(0,31):
            if(((i+3)%32 == j%32) or ((i+8)%32 == j%32)):
                graphG[i][j] = True
    return graphG

#Function to create an expression to later use for BDD
def createExpr(nodeVal, var):
    #nodeBinary = bin(nodeVal) #doesn't work properly

    #nodeBits is the binary represntaion of our values from 0-31
    nodeBinary = format(nodeVal, 'b').rjust(5, '0')
    #print("TestCases In nodeExpr idBin: "+ nodeBinary)

    BDDString = []
    for i in range(5):
        nodeName = f"{var*2}{i}"
        if((int(nodeBinary[i])) == 1):
            # print("if")
            # print(int(nodeBinary[i]))
            BDDString.append(nodeName)
        else:
            # print("else")
            # print(int(nodeBinary[i]))
            BDDString.append(f"~{nodeName}")
    return expr("&".join(BDDString))

#Creates a BDD expresion for our nodes
def createBDDString(nodeList, var):
    bddExprList = []
    for i in range(len(nodeList)):
        if(nodeList[i]):
            bddExprList.append(createExpr(i,var))
    #print("In creatBDD bddExprList: ")
    #print(bddExprList)
    bddString1 = bddExprList[0]
    #print(bddString1)
    for i in bddExprList[1:]:
        bddString1 |= i
    #print(bddString1)
    return expr2bdd(bddString1)

#searches for a spefic node
def findNode(bdd, nodeVal, var):
    nodeBinary = format(nodeVal, 'b').rjust(5, '0')
    varList = [bddvar(f"{var*2}" + str(i)) for i in range(5)]
    # print(nodeBinary)
    # print(varList)
    targetNode = {}
    for i in range(5):
        #print(targetNode)
        targetNode[varList[i]] = int(nodeBinary[i])
    #.restricpt and .is_one refrenced in the pyEDA documentaiuons
    #print(targetNode)
    resAns = bdd.restrict(targetNode)
    #print(resAns)
    return resAns.is_one()

#Searches for a spefic edge
def findEdge(bdd, nodeX, nodeY):
    nodeXBinary = format(nodeX, 'b').rjust(5, '0')
    nodeYBinary = format(nodeY, 'b').rjust(5, '0')

    varXList = [bddvar(f"{'x'*2}" + str(i)) for i in range(5)]
    varYList = [bddvar(f"{'y'*2}" + str(i)) for i in range(5)]

    targetEdge = {}
    for i in range(5):
        targetEdge[varXList[i]] = int(nodeXBinary[i])
        targetEdge[varYList[i]] = int(nodeYBinary[i])
    resAns = bdd.restrict(targetEdge)
    return resAns.is_one()

def graphToBDD(graphG):
    R = []
    for i in range(32):
        for j in range(32):
            if(graphG[i][j]):
                nodeX = createExpr(i,'x')
                nodeY = createExpr(j,'y')
                R.append(nodeX & nodeY)
    bddString1 = R[0]
    for i in R[1:]:
        bddString1 |= i
    return expr2bdd(bddString1)

def bddRR2(orginalRR):
    tmpVarList = [bddvar(f"{'z'*2}" + str(i)) for i in range(5)]
    varXList = [bddvar(f"{'x'*2}" + str(i)) for i in range(5)]
    varYList = [bddvar(f"{'y'*2}" + str(i)) for i in range(5)]

    composedSetRR1 = orginalRR.compose({varXList[i]: tmpVarList[i] for i in range(5)})
    composedSetRR2 = orginalRR.compose({varYList[i]: tmpVarList[i] for i in range(5)})

    return(composedSetRR1 & composedSetRR2).smoothing(tmpVarList)

    # for i in range(5):
    #     composedSetRR1 = orginalRR.compose({varXList[i]})

def bddRR2star(rr2):
    while True:
        prevRR2 = rr2
        rr2 = bddRR2(rr2)
        if(rr2.equivalent(prevRR2)):
            break
    return rr2





class TestGraph(unittest.TestCase):
    def testEVEN(self):
        #These tests are the given test in the assignment page

        # If I don't have this list here gives error
        # even though I declared it already
        self.evenList = [True if i % 2 == 0 else False for i in range(32)]
        evenBDD = createBDDString(self.evenList, 'x')

        #EVEN(14) Test
        nodeFound = findNode(evenBDD,14,'x')
        self.assertTrue(nodeFound)

        #EVEN(13) Test
        nodeNotFound = findNode(evenBDD,13,'x')
        self.assertFalse(nodeNotFound)

    def testPRIME(self):
        primeList = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        newPrimeList = [True if i in primeList else False for i in range(32)]

        primeBDD = createBDDString(newPrimeList, 'y')
        #print(primeBDD)

        #PRIME(7) Test
        nodeFound = findNode(primeBDD,7,'y')
        self.assertTrue(nodeFound)

        #PRIME(2) Test
        nodeNotFound = findNode(primeBDD,2,'y')
        self.assertFalse(nodeNotFound)

    def testRR(self):

        graphG = initGraph()

        rrBDD = graphToBDD(graphG)
        #print(rrBDD)

        #RR(27,3) Test
        edgeFound = findEdge(rrBDD,27,3)
        self.assertTrue(edgeFound)

        #RR(16,20) Test
        edgeNotFound = findEdge(rrBDD,16,20)
        self.assertFalse(edgeNotFound)

    def testRR2(self):
        graphG = initGraph()

        rr1 = graphToBDD(graphG)
        rr2 = bddRR2(rr1)

        #RR2(27,6) Test
        edgeFound = findEdge(rr2,27,6)
        self.assertTrue(edgeFound)

        #RR2(27,9) Test
        edgeNotFound = findEdge(rr2,27,9)
        self.assertFalse(edgeNotFound)

    def testRR2star(self):
        graphG = initGraph()
        rr1 = graphToBDD(graphG)
        rr2 = bddRR2(rr1)
        rr2star = bddRR2star(rr2)
        edgeFound = findEdge(rr2star, 27,6)
        self.assertTrue(edgeFound)

    def testStatemnt(self):
        graphG = initGraph()
        primeList = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        newPrimeList = [True if i in primeList else False for i in range(32)]
        evenList = [True if i % 2 == 0 else False for i in range(32)]
        varX = [bddvar(f"{'x'*2}" + str(i)) for i in range(5)]
        varY = [bddvar(f"{'y'*2}" + str(i)) for i in range(5)]

        rr1 = graphToBDD(graphG)
        rr2 = bddRR2(rr1)
        rr2star = bddRR2star(rr2)

        primeBDD = createBDDString(newPrimeList, 'x')
        evenBDD = createBDDString(evenList, 'y')
        evenNodesSteps = evenBDD & rr2star

        #Could not figure out how to procede from here got stuck on 
        #How I can further figure out if there are an even number of
        #Steps !!!!!!

        



if __name__ == "__main__":
    #evenList = [x for x in range(33) if (x%2 == 0)]
    #primeList = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    #print(varX)
    #print(varY)
    
    unittest.main()