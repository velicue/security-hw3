import string
import random
from random import randint
import csv
import sys
import numpy
import pickle
from collections import defaultdict
from datetime import date
import numpy.random as nprand


from pwtweak import gen_honeyword




### Util ###

def get_char_type(char):
    if char in string.ascii_letters:
        return 0
    elif char in string.digits:
        return 1
    else:
        return 2

def get_token_name(token):
    return str(get_char_type(token[0])) + str(len(token))

def write_csv(filename, values):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(values)

### File Parse ###

def read_rockyou_file():
    with open("rockyou-withcount.txt") as f:
        return [i.split() for (j, i) in enumerate(f.readlines()) if j < 100 and len(i.split()) == 2]

def read_input_file(filename):
    with open(filename) as f:
        return [i.strip() for i in f.readlines() if len(i.strip()) > 0]

### Password Generation ###

def generate_passwords(input_file, number=10):
    input_data = read_input_file(input_file)
    print len(input_data) 
    #sweetwords = [make_password(start, term, i, number) for i in input_data]
    return input_data

leetDict = {"a": "@", "@":"a", "s": "$","$":"s" ,"e": "3","3":"e", "t": "7", "7":"t", "o": "0","0":"o" ,"i": "|", "|":"i", "1":"l", "l":"1"}

def getEditingDistance(word1, word2):
    len_1 = len(word1)
    len_2 = len(word2)
    x =[[0] * (len_2 + 1) for _ in range(len_1 + 1)]#the matrix whose last element ->edit distance
    for i in range(0, len_1 + 1): #initialization of base case values
        x[i][0] = i
    for j in range(0, len_2 + 1):
        x[0][j] = j
    for i in range (1, len_1 + 1):
        for j in range(1, len_2 + 1):
            if word1[i - 1] == word2[j - 1]:
                x[i][j] = x[i - 1][j - 1] 
            elif word1[i - 1].lower() == word2[j - 1].lower():
                x[i][j] = x[i - 1][j - 1] + 1
            elif word1[i - 1].lower() in leetDict and leetDict[word1[i - 1].lower()] == word2[j - 1].lower():
                x[i][j] = x[i - 1][j - 1] + 2
            else:
                x[i][j] = min(x[i][j - 1], x[i - 1][j], x[i - 1][j - 1]) + 6
    return x[i][j]

def get_honeywords(n, password, common_passwords):
    honeywords = [password]

    found = 0
    for word in common_passwords:
        t = getEditingDistance(word, password)
        if t == 0:
            found = 1
            break
        if t <= len(word):
            found = 2

    if found == 1:
        # then return n randomly chosen passwords
        #print 'password: ' , password
        for h in range(int(n)):
            w = password
            while(w in honeywords):
                w = common_passwords[randint(0,len(common_passwords)-1)]    
            #print w   
            honeywords += [w]
        return honeywords
    elif found == 2:
        for h in range(int(n)):
            w = gen_honeyword(common_passwords[randint(0,len(common_passwords)-1)])   
            #print w   
            honeywords += [w]
        return honeywords
    else:
        for i in range(int(n)):
            honeywords += [gen_honeyword(password)]
        return honeywords


if len(sys.argv) != 4:
    print "Generate the honeywords."
    print ""
    print "python question2.py n inputfile outputfile"
    print ""
    print "     n               the number of passwords"
    print "     inputfile       the filename of inputfile"
    print "     outputfile      the filename of outputfile"
    sys.exit(1)
    
    
common_passwords = numpy.asarray(read_rockyou_file())[0:100,1]
print 'imported', len(common_passwords) , 'common passwords'
passwords = read_input_file(sys.argv[2])
print 'imported', len(passwords) , 'passwords to tweak'
#common_passwords = ['123456','12345','abcdefg']
#if len(passwords) == 0:
#passwords = ['123456','12345','123inputfile'] 

honeywords = []

for password in passwords:
    print 'password: ' , password
    b = get_honeywords(int(sys.argv[1]), password, common_passwords)
    print b
    honeywords.append( b )

        

print honeywords
write_csv( sys.argv[3] , honeywords)


#sweetwords = generate_passwords(sys.argv[2], int(sys.argv[1]))
#write_csv(sys.argv[3], sweetwords)

# python question2.py 5 rockyou-withcount.txt honeywords.txt


