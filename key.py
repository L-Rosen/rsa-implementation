# Generation de p et q étant premiers
# n = pq ; phi(n) = (p-1) * (q-1)
# generation de e premier avec phi(n) e < phi(n)
# trouve d avec euclide étendu
from math import sqrt
import random

# Définition des couleurs ANSI
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"

def colorPrint(color,text):
      print(color+text+RESET)

def isPrime(n):
        if n <= 1:return False

        if n == 2:return True

        if n%2 == 0:return False

        limit = int(sqrt(n)+1)
        for x in range(3,limit,2):
               if n%x == 0:
                     return False

        return True

def pqGen(lenght):
        p, q = 0, 0
        limit = 2**(lenght//2)
        while not isPrime(p):
              p = random.randint(2,limit)
        while not isPrime(q) or p == q:
              q = random.randint(2,limit)
        return p,q 

def phiCalc(p,q): 
      return(p-1)*(q-1)            
            
def extendedEuclid(a, b):
      r,r1,u,u1,v,v1 = a,b,1,0,0,1
      while r1 != 0: 
            q = (r // r1)
            r,u,v,r1,u1,v1 = r1,u1,v1,(r-q*r1),(u-q*u1),(v-q*v1)
      return r, u % b

def edGen(phi):
    e,d,r = 0,0,0
    while r != 1 or e == d:
        e = random.randint(2, phi-1)
        r, d = extendedEuclid(e, phi)
    return e, d

def encrypt(m, e, n): #C = M^e mod n
      return pow(m,e,n)

def decrypt(c, d, n): #M = C^d mod n
      return pow(c,d,n)

def keygen(lenght):
      p,q = pqGen(lenght)
      n = p*q
      phi = phiCalc(p,q)
      e,d = edGen(phi)

      print("p :",p)
      print("q :",q)
      print("n :",n)
      print("phi :",phi)
      print("e :",e)
      print("d :",d)

      return e,d,n,phi

def encrypt(m,e,n): return pow(m,e,n)
def decrypt(c,d,n): return pow(c,d,n)

e,d,n,phi = keygen(110)
m = random.randint(2,phi-1)
c = encrypt(m,e,n)
m1 = decrypt(c,d,n)
colorPrint(GREEN,f"Message : {m}")
colorPrint(YELLOW,f"Message chiffré : {c}")
colorPrint(GREEN, f"Message déchiffré : {m1}")