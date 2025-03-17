# Generation de p et q étant premiers
# n = pq ; phi(n) = (p-1) * (q-1)
# generation de e premier avec phi(n) e < phi(n)
# trouve d avec euclide étendu
from math import sqrt
import random
from hashlib import sha256

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
      return e,d,n,phi

def encrypt(m,e,n): return pow(m,e,n)
def decrypt(c,d,n): return pow(c,d,n)


def factorize(n):
      for p in range(1,n):
            q = n//p
            if isPrime(p) and isPrime(q) and n%p == 0:
                  return p,q

"""
Implémentation

e,d,n,phi = keygen(110)
m = random.randint(2,phi-1)
c = encrypt(m,e,n)
m1 = decrypt(c,d,n)
colorPrint(GREEN,f"Message : {m}")
colorPrint(YELLOW,f"Message chiffré : {c}")
colorPrint(GREEN, f"Message déchiffré : {m1}")
"""

"""
Test avec une clé de taille petite

e = 12413
p,q = factorize(13289)
n = p*q
phi = phiCalc(p,q)
r, d = extendedEuclid(e, phi)
m = [9197, 6284, 12836, 8709, 4584, 10239, 11553, 4584, 7008, 12523,
     9862, 356, 5356, 1159, 10280, 12523, 7506, 6311]

colorPrint(GREEN,f"Message non chiffré :\n")
for message in m:
      print(message,end=" ; ")

print()
colorPrint(YELLOW,f"Message déchiffré :\n")
for message in m:
      print(decrypt(message,d,n),end=" ; ")

print()
colorPrint(GREEN,f"Message re-chiffré :\n")
for message in m:
      print(encrypt(decrypt(message,d,n),e,n),end=" ; ")

La complexité est de n*sqrt(n)
"""

"""
e = 163119273
p,q = factorize(755918011)
n = p*q
phi = phiCalc(p,q)
r, d = extendedEuclid(e, phi)
m = [671828605, 407505023, 288441355, 679172842, 180261802]

colorPrint(GREEN,f"Message non chiffré :\n")
for message in m:
      print(message,end=" ; ")

print()
colorPrint(YELLOW,f"Message déchiffré :\n")
for message in m:
      print(decrypt(message,d,n),end=" ; ")

print()
colorPrint(GREEN,f"Message re-chiffré :\n")
for message in m:
      print(encrypt(decrypt(message,d,n),e,n),end=" ; ")
"""

def replaceAlphabet(alphabet,letter): return alphabet[letter]

def replaceNumber(alphabet, number): 
      for letter in alphabet:
            if alphabet[letter] == number:
                  return letter

def blockSizeCalc(n,alphabet):
      i = 1
      while len(alphabet)**i < n:
            i = i+1
      return i-1

def letterToNumber(alphabet, i, letter): 
      return replaceAlphabet(alphabet,letter)*(len(alphabet)**i)

def messageToBlocks(message,alphabet,block_size):

      blocks = []
      somme = 0
      i = block_size
      for letter in message:
            i = i-1
            somme += letterToNumber(alphabet, i, letter)
            if i == 0:
                  blocks.append(somme)
                  i = block_size
                  somme = 0

      if i > 0:
            for j in range(i):
                  i -= 1
                  somme+= letterToNumber(alphabet, i, ' ')
            blocks.append(somme)
      return blocks

def blocksToMessage(blocks, alphabet, block_size):
      message = ""
      for block in blocks:
            block_sum = block
            for i in range(block_size,0,-1):
                  calc = block_sum // (len(alphabet)**(i-1))
                  block_sum = block_sum % (len(alphabet)**(i-1))
                  message += replaceNumber(alphabet,calc)
      return message

def encryptBlocks(blocks,e,n):
      blocksBis = []
      for m in blocks:
            blocksBis.append(encrypt(m,e,n))
      return blocksBis

def decryptBlocks(blocks,d,n):
      blocksBis = []
      for c in blocks:
            blocksBis.append(decrypt(c,d,n))
      return blocksBis

"""
RSA ET CODAGE
alphabet = {
      "a": 0,
      "b": 1,
      "c": 2,
      "d": 3,
      "e": 4,
      "f": 5,
      "g": 6,
      "h": 7,
      "i": 8,
      "j": 9,
      "k": 10,
      "l": 11,
      "m": 12,
      "n": 13,
      "o": 14,
      "p": 15,
      "q": 16,
      "r": 17,
      "s": 18,
      "t": 19,
      "u": 20,
      "v": 21,
      "w": 22,
      "x": 23,
      "y": 24,
      "z": 25,
      "A": 26,
      "B": 27,
      "C": 28,
      "D": 29,
      "E": 30,
      "F": 31,
      "G": 32,
      "H": 33,
      "I": 34,
      "J": 35,
      "K": 36,
      "L": 37,
      "M": 38,
      "N": 39,
      "O": 40,
      "P": 41,
      "Q": 42,
      "R": 43,
      "S": 44,
      "T": 45,
      "U": 46,
      "V": 47,
      "W": 48,
      "X": 49,
      "Y": 50,
      "Z": 51,
      " ": 52,
      ".": 53,
      ",": 54,
      ";": 55,
      ":": 56,
      "!": 57,
      "?": 58,
      "'": 59
}

print(YELLOW,end="")
e,d,n,phi = keygen(int(input("Taille de la clé : ")))

print(RESET,end="")
colorPrint(CYAN,f"Clé publique : {e,n}")
colorPrint(CYAN,f"Clé privée : {d,n}")
colorPrint(CYAN,f"Phi : {phi}\n")
print(YELLOW,end="")

message = input("Message a chiffrer: ")
print(RESET,end="")

blockSize = blockSizeCalc(n,alphabet)
colorPrint(CYAN,f"Taille des blocs : {blockSize}\n")

blocks = messageToBlocks(message,alphabet,blockSize)
colorPrint(GREEN,f"Message : {message}")
colorPrint(GREEN,f"Message en blocs : {blocks}\n")

blocks = encryptBlocks(blocks,e,n)
blocks_bis = blocksToMessage(blocks,alphabet,blockSize+1)
colorPrint(RED,f"Message chiffré : {blocks_bis}")
colorPrint(RED,f"Message chiffré en blocks : {blocks}\n")

blocks = decryptBlocks(blocks,d,n)
colorPrint(GREEN,f"Message déchiffré en blocs: {blocks}")
colorPrint(GREEN,f"Message déchiffré : {blocksToMessage(blocks,alphabet,blockSize)}")"
"""

def hashFile(file):
      with open(file,"rb") as f:
            return sha256(f.read()).hexdigest()

def signHash(hash,d,n):
      alphabet_hex = {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "a": 10,
            "b": 11,
            "c": 12,
            "d": 13,
            "e": 14,
            "f": 15,
            " ": 16
      }

      block_size = blockSizeCalc(n,alphabet_hex)
      blocks = messageToBlocks(hash,alphabet_hex,block_size)
      encrypt_blocks = encryptBlocks(blocks,d,n)
      return encrypt_blocks

def verifyHash(hash,signature,e,n):
      alphabet_hex = {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "a": 10,
            "b": 11,
            "c": 12,
            "d": 13,
            "e": 14,
            "f": 15,
            " ": 16
      }

      block_size = blockSizeCalc(n,alphabet_hex)
      blocks = decryptBlocks(signature,e,n)
      message = blocksToMessage(blocks,alphabet_hex,block_size).replace(" ","")
      return message == hash

e,d,n,phi = keygen(32)
hash = hashFile("input.txt")
signature = signHash(hash,d,n)
verifyHash(hash,signature,e,n)

colorPrint(CYAN,f"Hash : {hash}")
colorPrint(CYAN,f"Signature : {signature}")

if verifyHash(hash,signature,e,n):
      colorPrint(GREEN,"Signature valide")
else:
      colorPrint(RED,"Signature invalide")