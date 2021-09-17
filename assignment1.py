
#from numpy import *
# index for blood types: O-,O+,A-,A+,B-,B+,AB-,AB+, column: donor, row: recipient
table = [ [1,0,0,0,0,0,0,0],
          [1,1,0,0,0,0,0,0],
          [1,0,1,0,0,0,0,0],
          [1,1,1,1,0,0,0,0],
          [1,0,0,0,1,0,0,0],
          [1,1,0,0,1,1,0,0],
          [1,0,1,0,1,0,1,0],
          [1,1,1,1,1,1,1,1]
        ]

def truth_table(donor,recp):
  print(table[donor][recp])

def boolean_circuit(a,b,c,d,e,f):
    #ret = (int(not(r_2*r_1*r_0))+ d_0*int(not(r_1*r_0)) + d_1*int(not(r_2*r_0)) + d_2*int(not(r_1*r_0)) + d_1*d_0*int(not(r_2))+d_2*d_0*int(not(r_1))+(d_2*d_1*int(not(r_0)))+(d_2*d_1*d_0))
    ret = ((int(not(d)))*(int(not(e)))*(int(not(f)))) + (c*(int(not(d)))*(int(not(e)))) + (b*int(not(d))*int(not(f))) + (b*c*int(not(d))) + (a*int(not(e))*int(not(f))) + (a*c*(int(not(e)))) + (a*b*int(not(f))) + (a*b*c)
    print(ret%2)
print("O-:000,...,AB+:111")
print("Enter bit representation for donor blood type...")
d_2 = int(input("msb bit: "))
d_1 = int(input("second bit: "))
d_0 = int(input("lsb bit: "))
print("Enter bit representation for recipient blood type...")
r_2 = int(input("msb bit: "))
r_1 = int(input("second bit: "))
r_0 = int(input("lsb bit: "))
print(truth_table(r_2*4+r_1*2+r_0,d_2*4+d_1*2+d_0))
print(boolean_circuit(r_2,r_1,r_0,d_2,d_1,d_0))
