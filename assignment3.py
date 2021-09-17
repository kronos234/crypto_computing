#Author: Mahak Pancholi
import random

from pprint import pprint

#Truth table for blood type function
         #O-,O+,A-,A+,B-,B+,AB-,AB+
T =     [ [1,0,0,0,0,0,0,0], #O-
          [1,1,0,0,0,0,0,0], #O+
          [1,0,1,0,0,0,0,0], #A-
          [1,1,1,1,0,0,0,0], #A+
          [1,0,0,0,1,0,0,0], #B-
          [1,1,0,0,1,1,0,0], #B+
          [1,0,1,0,1,0,1,0], #AB-
          [1,1,1,1,1,1,1,1]  #AB+
        ]

def build_input(b_2,b_1,b_0):
    #xA is 1 if the group is A or AB and 0 otherwise
    if  ((b_1 == 1)and (b_0 == 1)) or((b_2==1)and(b_1==1)and(b_0==1)):
        b_A = 1
    else:
        b_A = 0
    #xB is 1 if the group is B or AB and 0 otherwise
    if ((b_2==1)and(b_0==1)) or ((b_2==1)and(b_1==1)and(b_0==1)):
        b_B=1
    else:
        b_B =0
    #bit xR is 1 if the Rh is + and 0 otherwise.
    if ((b_2==0)and(b_1==0)and(b_0==1)) or ((b_2==0)and(b_1==1)and(b_0==1)) or ((b_2==1)and(b_1==0)and(b_0==1)) or ((b_2==1)and(b_1==1)and(b_0==1)):
        b_R = 1
    else:
        b_R = 0

    return [b_A,b_B,b_R]

class Alice:
    #initialization for Alice
    def __init__(self,n,x,D):
        self.n = n
        #Note that u_B,v_B,w_B here are arrays of length 5
        self.triple = D.TripleA()
        self.u = self.triple[0]
        self.v = self.triple[1]
        self.w = self.triple[2]
        self.input = x
        self.out = None
        self.G1 = None
        self.G2 = None
        self.G3 = None
        self.G4 = None
        self.G5 = None
        self.inputB = None

    def share_input(self):
        self.inputA = random.getrandbits(self.n)
        return self.inputA^self.input


class Bob:
    def __init__(self,n,y,D):
        self.n = n
        #Note that u_B,v_B,w_B here are arrays of length 5
        self.triple = D.TripleB()
        self.u = self.triple[0]
        self.v = self.triple[1]
        self.w = self.triple[2]
        self.input = y
        self.out = None
        self.G1 = None
        self.G2 = None
        self.G3 = None
        self.G4 = None
        self.G5 = None
        self.inputA = None


    def share_input(self):
        self.inputB = random.getrandbits(self.n)
        return self.inputB^self.input




class Dealer: # generates random beaver triples
    def __init__(self,n):
        self.n = n
        self.u = [0 for i in range(5)]
        self.v = [0 for i in range(5)]
        self.w = [0 for i in range(5)]
        #Alice's shares
        self.u_A = [0 for i in range(5)]
        self.v_A = [0 for i in range(5)]
        self.w_A = [0 for i in range(5)]
        #Bob's shares
        self.u_B = [0 for i in range(5)]
        self.v_B = [0 for i in range(5)]
        self.w_B = [0 for i in range(5)]

        for i in range(5):
            self.u[i] = random.getrandbits(self.n) #get random u
            self.v[i] = random.getrandbits(self.n) #get random v
            self.w[i] = self.u[i]&self.v[i]
        for i in range(5):
            self.u_A[i] = random.getrandbits(self.n)
            self.u_B[i] = self.u[i]^self.u_A[i]
            self.v_A[i] = random.getrandbits(self.n)
            self.v_B[i] = v^self.v_A[i]
            self.w_A[i] = random.getrandbits(self.n)
            self.w_B[i] = w^self.w_A[i]

    def TripleA(self):
        return [self.u_A,self.v_A,self.w_A]

    def TripleB(self):
        return [self.u_B,self.v_B,self.w_B]


#input sharing function
def input_sharing(A,B):
    A.inputB =  B.share_input()#Alice's share of Bob's input
    B.inputA =  A.share_input()#Bob's share of Alice's input





if __name__ == '__main__':
    n = 3
    #formula: (1^(x_A&(1^y_A)))&(1^(x_B&(1^y_B)))&(1^(x_R&(1^y_R)))
    print("")
    print("Blood type is encoded as: O-:000,...,AB+:111")
    print("Alice's output is:")
    for x_2 in range(2):
        for x_1 in range(2):
            for x_0 in range(2):
                for y_2 in range(2):
                    for y_1 in range(2):
                        for y_0 in range(2):
                            D = Dealer(n)
                            input_x = build_input(x_2,x_1,x_0)
                            input_y = build_input(y_2,y_1,y_0)
                            A = Alice(n,input_x,D) #beaver triples created for Alice
                            B = Bob(n,input_y,D)   #beaver triples created for Alice
                            #Sharing input
                            input_sharing(A,B)
                            #Computing first layer of and gates:  G1 = x_A&(1^y_A) ; G2 = x_B&(1^y_B) and G3 = x_R&(1^y_R)
                            #level1(A,B)
                            #Computing second layer of and gates: G4 = (1^(G1))&(1^G2)
                            #level2(A,B)
                            #Computing third layer of and gates: G5 = G4 &(1^G3)
                            #level3(A,B)
                            #print output
                            print(A.inputB)
                            print(A.inputA)
                            print(B.inputA)
                            print(B.inputB)
