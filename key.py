# Generation de p et q étant premiers
# n = pq ; phi(n) = (p-1) * (q-1)
# generation de e premier avec phi(n) e < phi(n)
# trouve d avec euclide étendu
from math import sqrt
import random
from tqdm import tqdm

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
        if n <= 1: 
              return False

        if n == 2 : 
              colorPrint(GREEN,f"{n} est premier.\n")
              return True

        if n%2 == 0: 
              return False #On élimine les nombres pairs sauf 2 avant d'itérer

        for x in tqdm(range(3,int(sqrt(n))+1,2),f"Verification de {n}",unit="test"):
               if n%x == 0: 
                     return False

        colorPrint(GREEN,f"{n} est premier.\n")
        return True

def pqGen(lenght):
        p, q = 0, 0

        colorPrint(CYAN,"Génération de p ...")
        while not isPrime(p):
            p = random.randint(2,2**(lenght//2))

        colorPrint(CYAN,"Génération de q ...")
        while not isPrime(q) or p == q:
            q = random.randint(2,2**(lenght//2))
        
        return p,q 

def phiCalc(p,q):
       return(p-1)*(q-1)            

            
def extendedEuclid(e, phi):
    a, b = e, phi
    u0, u1 = 1, 0
    while b != 0:
        q, a, b = a // b, b, a % b
        u0, u1 = u1, u0 - q * u1
    if a != 1:
        return False, None
    
    d = u0 % phi
    return True, d
    

def edGen(phi):
    e = 0
    colorPrint(CYAN, "Génération de e , d...")
    isPrimeTogether = False
    while not isPrimeTogether:
        e = random.randint(2, phi)
        isPrimeTogether, d = extendedEuclid(e, phi)
    
    colorPrint(GREEN, f"e = {e} est premier avec phi(n) = {phi}.")
    colorPrint(GREEN, f"d = {d} est l'inverse modulaire de {e}.\n")
    return e, d

def encrypt(m, e, n): #C = M^e mod n
      return pow(m,e,n)

def decrypt(c, d, n): #M = C^d mod n
      return pow(c,d,n)
    

p,q = pqGen(64)
n = p*q
phi = phiCalc(p,q)
e,d = edGen(phi)
print("p :",p)
print("q :",q)
print("n :",n)
print("phi :",phi)
print("e :",e)
print("d :",d)

colorPrint(CYAN,"Test de chiffrement et dechiffrement ...")
m = random.randint(2,n-1)
print(f"Message : {m}")
c = encrypt(m,e,n)
print(f"Message chiffré : {c}")
m = decrypt(c,d,n)
print(f"Message déchiffré : {m}")

