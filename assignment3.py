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
    #add conditions for x_A,...
    if  ((b_1 = 1)and (b_0 = 1)) or((b_2=1)and(b_1=1)and(b_0=1)):#xA is 1 if the group is A or AB and 0 otherwise
        b_A = 1
    else:
        b_A = 0

    if ((b_2=1)and(b_0=1)) or ((b_2=1)and(b_1=1)and(b_0=1)): #xB is 1 if the group is B or AB and 0 otherwise
        b_B=1
    else:
        b_B =0
    #bit xR is 1 if the Rh is + and 0 otherwise.
    if ((b_2=0)and(b_1=0)and(b_0=1)) or ((b_2=0)and(b_1=1)and(b_0=1)) or ((b_2=1)and(b_1=0)and(b_0=1)) or ((b_2=1)and(b_1=1)and(b_0=1)):
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
        self.u_A = self.triple[0]
        self.v_A = self.triple[1]
        self.w_A = self.triple[2]
        self.input = x
        self.out = None

    def share_input(self):

    def xor(self):

    def and(self):

    def mult_by_const(self):

    def add_by_const(self):

    def send(self):

    def receive(self, msg):

    def output(self):
        return self.out

class Bob:
    def __init__(self,n,y,D):
        self.n = n
        #Note that u_B,v_B,w_B here are arrays of length 5
        self.triple = D.TripleB()
        self.u_B = self.triple[0]
        self.v_B = self.triple[1]
        self.w_B = self.triple[2]
        self.input = y
        self.out = None

    def share_input(self):
        self.inputy_B = random.getrandbits(self.n)
        self.inputy_A = self.inputy_B^self.input

    def xor(self):

    def and(self):

    def mult_by_const(self):

    def add_by_const(self):

    def send(self):
        return [self.v,self.z_B]

    def receive(self,msg):

    def output(self):




class Dealer: # generates random beaver triples
    def __init__(self,n):
        self.n = n
        self.u = [0 for i in range(5)]
        self.v = [0 for i in range(5)]
        self.w = [0 for i in range(5)]

    def generate_triple(self):
        #for loop for number of and gates in the formula:
        for i in range(5):
            self.u[i] = random.getrandbits(self.n) #get random u
            self.v[i] = random.getrandbits(self.n) #get random v
            self.w[i] = u&v

    def share_triple(self):
        for i in range(5):
            self.u_A[i] = random.getrandbits(self.n)
            self.u_B[i] = u^self.u_A[i]
            self.v_A[i] = random.getrandbits(self.n)
            self.v_B[i] = v^self.v_A[i]
            self.w_A[i] = random.getrandbits(self.n)
            self.w_B[i] = w^self.w_A[i]

    def TripleA(self):
        return [self.u_A,self.v_A,self.w_A]

    def TripleB(self):
        return [self.u_B,self.v_B,self.w_B]



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
                            B.receive(A.send(A.share_input())) #Alice shares her input
                            A.receive(B.send(B.share_input())) #Bob shares his input




            B.receive(A.send()) #Bob receives first message from Alice
            A.receive(B.send()) #Alice receives second round message from Bob
            print("Compatibility of: ", x, " and ", y, " is ", A.output()) #Alice computes output
