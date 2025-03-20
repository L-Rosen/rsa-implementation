# Generation de p et q étant premiers
# n = pq ; phi(n) = (p-1) * (q-1)
# generation de e premier avec phi(n) e < phi(n)
# trouve d avec euclide étendu
from math import sqrt
import random
from hashlib import sha256
import argparse

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

def messageToBlocks(message,alphabet,block_size,autofillChar):

        blocks = []
        i = 0
        while i < len(message):
                block = 0
                letter = ""
                for j in range(block_size,0,-1):
                    if i < len(message):
                            letter += message[i]
                            block += letterToNumber(alphabet,j-1,message[i])
                            i += 1
                    else:
                            block += letterToNumber(alphabet,j-1,autofillChar)
                blocks.append(block)
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

def hashFile(file):
      with open(file,"rb") as f:
            content = f.read()
            h = sha256(content).hexdigest()
            hint = int(h,16)
            return hint

def sign(file,d,n):
      h = hashFile(file) % n
      return encrypt(h,d,n)

def verify(file,signature,e,n):
      h = hashFile(file) % n
      return h == decrypt(signature,e,n)

if __name__ == "__main__":
      parser = argparse.ArgumentParser(description="Outil RSA en ligne de commande")
      parser.add_argument("mode", choices=["keygen", "encrypt", "decrypt","factorize","sign","verify"], help="Action à effectuer")
      parser.add_argument("--keysize", type=int, help="Taille de la clé en bits", default=32)
      parser.add_argument("--key", type=int, help="Exposant pour chiffrer/déchiffrer")
      parser.add_argument("--n", type=int, help="Module n")
      parser.add_argument("--messageint", type=int, help="Message (nombre) à chiffrer/déchiffrer")
      parser.add_argument("--messagetxt", type=str, help="Message (texte) à chiffrer/déchiffrer")
      parser.add_argument("--file", type=str, help="Fichier à signer")
      parser.add_argument("--signature", type=str, help="Signature à vérifier")

      args = parser.parse_args()

      alphabet = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11, 
                        "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22,
                        "x": 23, "y": 24, "z": 25, "A": 26, "B": 27, "C": 28, "D": 29, "E": 30, "F": 31, "G": 32, "H": 33,
                        "I": 34, "J": 35, "K": 36, "L": 37, "M": 38, "N": 39, "O": 40, "P": 41, "Q": 42, "R": 43, "S": 44,
                        "T": 45, "U": 46, "V": 47, "W": 48, "X": 49, "Y": 50, "Z": 51, "_": 52, ".": 53, ",": 54, ";": 55,
                        ":": 56, "!": 57, "?": 58, "'": 59}

      if args.mode == "keygen":
            e,d,n,phi = keygen(args.keysize)
            print(f"Taille de la clé : {args.keysize}")
            print(f"Exposant publique : {e}")
            print(f"Exposant privé : {d}")
            print(f"Module n : {n}")
      
      elif args.mode == "encrypt":
            if not args.key or not args.n:
                  e,d,n,phi = keygen(args.keysize)
                  print(f"Aucune clé fournie , génération de clé aléatoire")
                  print(f"Clé publique : ({e},{n})")
                  print(f"Clé privée : ({d},{n})")
            else:
                  e,n = args.key,args.n

            if not args.messageint and not args.messagetxt: #Si aucun message n'est spécifié
                  print("Vous devez spécifier un message à chiffrer")
            
            elif args.messageint and args.messagetxt: #Si les deux types de messages sont spécifiés
                  print("Vous devez spécifier un seul type de message")

            elif args.messageint and not args.messagetxt: #Si le message est un nombre
                  encrypted = encrypt(args.messageint,e,n)
                  print(f"Message chiffré: {encrypted}")

            elif args.messagetxt and not args.messageint: #Si le message est un texte
                  blockSize = blockSizeCalc(n,alphabet)
                  blocks = messageToBlocks(args.messagetxt,alphabet,blockSize,"_")
                  encrypted = encryptBlocks(blocks,e,n)
                  print(f"Message chiffré : {blocksToMessage(encrypted,alphabet,blockSize+1)}")
                  
            
      elif args.mode == "decrypt":
            if not args.key or not args.n or (not args.messageint and not args.messagetxt):
                  print("Vous devez spécifier l'exposant de déchiffrement, le module et le message à déchiffrer")

            elif not args.messageint and not args.messagetxt: #Si aucun message n'est spécifié
                  print("Vous devez spécifier un message à déchiffrer")
            
            elif args.messageint and args.messagetxt: #Si les deux types de messages sont spécifiés
                  print("Vous devez spécifier un seul type de message")

            elif args.messageint and not args.messagetxt: #Si le message est un nombre
                  encrypted = encrypt(args.messageint,args.key,args.n)
                  print(f"Message déchiffré: {encrypted}")

            elif args.messagetxt and not args.messageint: #Si le message est un texte
                  blockSize = blockSizeCalc(args.n,alphabet)+1
                  blocks = messageToBlocks(args.messagetxt,alphabet,blockSize,"_")
                  decrypted = decryptBlocks(blocks,args.key,args.n)
                  print(f"Message déchiffré : {blocksToMessage(decrypted,alphabet,blockSize-1)}")
      
      elif args.mode == "factorize":
           if not args.n or not args.key or not args:
                    print("Vous devez spécifier le module et l'exposant pour l'attaque par factorisation")
           else:
                  p,q = factorize(args.n)
                  phi = phiCalc(p,q)
                  r, d = extendedEuclid(args.key, phi)
                  if args.message:
                        decrypt = decrypt(args.message,d,args.n)
                        reencrypt = encrypt(decrypt,args.key,args.n)

                  print(f"Clé fournie :({args.key},{args.n})")
                  print(f"Clé calculée : ({d},{args.n})")

                  if args.message:
                        if reencrypt != args.message :
                              print("Erreur lors de l'attaque par factorisation")
                        else:
                              print(f"Message déchiffré : {decrypt}")

      elif args.mode == "sign":
        if not args.file:
            print("Vous devez spécifier un fichier à signer")
        else:
            e,d,n,phi = None,args.key,args.n, None
            if not args.key or not args.n:
                e,d,n,phi = keygen(args.keysize)
                print(f"Aucune clé fournie, génération de clé aléatoire")
                print(f"Clé publique : ({e},{n})")
                print(f"Clé privée : ({d},{n})")

            signature = sign(args.file, d, n)
            print(f"Signature : {signature}")

      elif args.mode == "verify":
        if not args.file or not args.key or not args.n or not args.signature:
            print("Vous devez spécifier un fichier, une clé publique, le module n et la signature à vérifier")
        else:
            is_valid = verify(args.file, int(args.signature), args.key, args.n)
            if is_valid:
                print("Signature valide")
            else:
                print("Signature invalide")