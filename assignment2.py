#Author: Mahak Pancholi
import random

from pprint import pprint

#Truth table for blood type function
T = [ [1,0,0,0,0,0,0,0],
          [1,1,0,0,0,0,0,0],
          [1,0,1,0,0,0,0,0],
          [1,1,1,1,0,0,0,0],
          [1,0,0,0,1,0,0,0],
          [1,1,0,0,1,1,0,0],
          [1,0,1,0,1,0,1,0],
          [1,1,1,1,1,1,1,1]
        ]

class Alice:
    #initialization for Alice
    def __init__(self,n,x,D):
        self.n = n
        self.ret = D.RandA()
        self.r = self.ret[0]
        self.M_A = self.ret[1]
        self.input = x
        self.out = None

    def send(self):
        self.u = (self.input+self.r)%2**self.n
        return self.u

    def receive(self, msg):
        self.v = msg[0]
        self.z_B = msg[1]
        self.out = self.M_A[self.u][self.v]^self.z_B

    def output(self):
        return self.out

class Bob:
    def __init__(self,n,y,D):
        self.n = n
        self.ret = D.RandB()
        self.s = self.ret[0]
        self.M_B = self.ret[1]
        self.input = y
        self.z_B = None

    def send(self):
        return [self.v,self.z_B]

    def receive(self,msg):
        self.u = msg
        self.v = (self.input+self.s)%(2**n)
        self.z_B = self.M_B[self.u][self.v]




class Dealer:
    def __init__(self,n):
        self.M_A = [ [ 0 for i in range(2**n) ] for j in range(2**n) ]
        self.M_B = [ [ 0 for i in range(2**n) ] for j in range(2**n) ]
        self.n = n
        #initialization for Alice
        self.r = random.getrandbits(self.n)
        for i in range(2**self.n):
            for j in range(2**self.n):
                self.M_A[i][j]=random.getrandbits(1)
        #initialization for Bob
        self.s = random.getrandbits(self.n)
        for i in range(2**self.n):
            for j in range(2**self.n):
                self.M_B[i][j] = self.M_A[i][j]^T[i-self.r%(2**self.n)][j-self.s%(2**self.n)]

    def RandA(self):
        return [self.r,self.M_A]

    def RandB(self):
        return [self.s,self.M_B]



if __name__ == '__main__':
    n = 3
    print("")
    print("Blood type is encoded as: O-:000,...,AB+:111")
    print("Alice's output is:")
    for x in range(8):
        for y in range(8):
            D = Dealer(n)
            A = Alice(n,x,D) #get setup information for Alice from dealer
            B = Bob(n,y,D) #get setup information for Bob from dealer
            B.receive(A.send()) #Bob receives first message from Alice
            A.receive(B.send()) #Alice receives second round message from Bob
            print("Compatibility of: ", x, " and ", y, " is ", A.output()) #Alice computes output
