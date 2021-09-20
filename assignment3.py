import random
from pprint import pprint

_A, _B, _R = range(3)
ABR = [_A, _B, _R]

def create_rand_inp():
    return [random.getrandbits(1) for _ in [_A, _B, _R]]

# self.x = create_rand_inp()
# self.y = create_rand_inp()

def get_gate_index(index):
    if index == 9:
        i = 0
    if index == 10:
        i = 1
    if index == 11:
        i = 2
    if index == 14:
        i = 3
    if index == 16:
        i = 4
    return i

class Dealer: # generates random beaver triples
    def __init__(self,n):
        self.n = n
        self.u = [random.getrandbits(1) for _ in range(5)]
        self.v = [random.getrandbits(1) for _ in range(5)]
        self.w = [0 for i in range(5)]
        #Alice's triple shares
        self.u_A = [random.getrandbits(1) for _ in range(5)]
        self.v_A = [random.getrandbits(1) for _ in range(5)]
        self.w_A = [random.getrandbits(1) for _ in range(5)]
        #Bob's triple shares
        self.u_B = [0 for i in range(5)]
        self.v_B = [0 for i in range(5)]
        self.w_B = [0 for i in range(5)]

        for i in range(5):
            self.w[i] = self.u[i]&self.v[i]

        for i in range(5):
            self.u_B[i] = self.u[i]^self.u_A[i]
            self.v_B[i] = self.v[i]^self.v_A[i]
            self.w_B[i] = self.w[i]^self.w_A[i]

    def TripleA(self): #return ALice's triple share
        return [self.u_A,self.v_A,self.w_A]

    def TripleB(self):#return Bob's triple share
        return [self.u_B,self.v_B,self.w_B]

class Alice:
    #initialization for Alice
    def __init__(self,x,D):
        #Note that u_B,v_B,w_B here are arrays of length 5
        self.triple = D.TripleA()
        self.u = self.triple[0]
        self.v = self.triple[1]
        self.w = self.triple[2]
        self.input = x
        # No. of gates in the circuit are 17 (including input and xor gates)
        self.G = [0 for i in range(17)]
        for j in ABR:
            self.G[j] = random.getrandbits(1)

    def share_input(self): #share inputs with Bob
        return [self.input[j]^self.G[j] for j in ABR]

    def and_gate(self,val1,val2,index): #compute share of d, e
        i = get_gate_index(index)
        return [val1^self.u[i], val2^self.v[i]]

class Bob:
    def __init__(self,y,D):
        self.n = n
        #Note that u_B,v_B,w_B here are arrays of length 5
        self.triple = D.TripleB()
        self.u = self.triple[0]
        self.v = self.triple[1]
        self.w = self.triple[2]
        self.input = y
        self.G = [0 for i in range(17)]
        for j in ABR:
            self.G[j+3] = random.getrandbits(1)

    def share_input(self):
        return [self.input[j]^self.G[j+3] for j in ABR]

    def and_gate(self,val1,val2,index):
        i = get_gate_index(index)
        return [val1^self.u[i], val2^self.v[i]]

#This function generates input shares for both Alice and Bob
def input_sharing(A,B):
    B.G[0],B.G[1],B.G[2] = A.share_input()
    A.G[3],A.G[4],A.G[5] = B.share_input()

def compute_xor(A,B,c,index_in,index_out):
    A.G[index_out] = A.G[index_in]^c
    B.G[index_out] = B.G[index_in]

def compute_and(A,B, index_l,index_r,index_o):
    valA = A.and_gate(A.G[index_l],A.G[index_r],index_o)
    valB = B.and_gate(B.G[index_l],B.G[index_r],index_o)
    d =  valA[0]^valB[0]
    e =  valA[1]^valB[1]
    i = get_gate_index(index_o)
    A.G[index_o] = A.w[i]^(e&(A.G[index_l]))^(d&(A.G[index_r]))^(e&d) #Alice's share of gate index
    B.G[index_o] = B.w[i]^(e&(B.G[index_l]))^(d&(B.G[index_r])) #Bob's share of gate index

def layer1(A,B):
    compute_xor(A,B,1,3,6)
    compute_xor(A,B,1,4,7)
    compute_xor(A,B,1,5,8)
    compute_and(A,B,0,6,9)
    compute_and(A,B,1,7,10)
    compute_and(A,B,2,8,11)

def layer2(A,B):
    compute_xor(A,B,1,9,12)
    compute_xor(A,B,1,10,13)
    compute_and(A,B,12,13,14)

def layer3(A,B):
    compute_xor(A,B,1,11,15)
    compute_and(A,B,14,15,16)

def output(A,B):
    return A.G[16]^B.G[16]

if __name__ == '__main__':
    n = 3
    #formula: (1^(x_A&(1^y_A)))&(1^(x_B&(1^y_B)))&(1^(x_R&(1^y_R)))
    test_x = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
    test_y = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
    print("Alice's input, Bob's input, Compatibility output")
    for x in test_x:
        for y in test_y:
            D = Dealer(n)
            A = Alice(x,D)
            B = Bob(y,D)
            #wires as follow: (G[0]=x_A,G[1]=x_B,G[2]=x_R,G[3]=y_A,G[4]=y_B,G[5]=y_R,
            #G[6]=xor(1,G[3]),G[7]=xor(1^y_B),G[8]=xor(1^y_R),G[9]=and(G[0],G[6]),
            # G[10] = and(G[1],G[7]), G[11] = and(G[2],G[8]), G[12] = xor(1,G[9]),
            #G[13] = xor(1,G[10]), G[14] = and(G[12],G[13]), G[15] = xor(1,G[11]),
            #G[16] = and(G[14],G[15]).
            #sharing inputs: i.e shares og gates G0,G1...G5
            input_sharing(A,B)
            #Computing layer 1 of the circuit: gates G6,...G11
            layer1(A,B)
            #layer 2: gates G12...G14
            layer2(A,B)
            #layer 3: gates G15,G16
            layer3(A,B)
            print(x,y,output(A,B))
