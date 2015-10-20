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


def gen(pw, k, t):
    special_ex = '[~!@#$%^&*()_+{}":;\\\']+$'
    if t > len(pw):
        t = len(pw)
        
	
    honey_list = []
    for k in range(0,k):
		honey_tail = []
		for c in pw[-t:]:
			if c.isdigit():
				honey_tail.append(random.choice(string.digits) )
			elif c in special_ex:
				honey_tail.append(random.choice(special_ex) )
			else:
				honey_tail.append(random.choice(string.ascii_letters) )
		honey_list.append(pw[:len(pw)- t]+''.join(honey_tail))
    return honey_list
		

def gen_digits(pw, k):
    pw_seg, pw_seg_isdigit = pwSeperate(pw)
    pw_seg_cp = list(pw_seg)
    idx_list = []
    for idx, isdigit in enumerate(pw_seg_isdigit):
        if isdigit :
            idx_list.append(idx)

    honey_list = []
    for k in xrange(0, k):
        for idx in idx_list:
            seg = pw_seg[idx]
            if (len(seg)==4 and ((seg[0:2] == "19") or (seg[0:2] == "20")) ):
                pw_seg_cp[idx] = str(random.choice(range(1900, date.today().year)))
            else:
                randnu = random.randint(0, 10**len(seg) - 1)
                pw_seg_cp[idx] = str(randnu)
        honey_list.append(''.join(pw_seg_cp))
    return honey_list

def gen_rand(pw, k):
    special_ex = ')!@#$%^&*([~_+{}":;\\\']+$'

    honey_list = []
    for k in range(0,k):
        honey_tail = []
        for c in pw:
            if c.isdigit():
                die = random.randint(0,3)
                if(die == 0):
                    honey_tail.append(random.choice(string.digits) )
                elif (die == 1):
                    honey_tail.append(c)
                    honey_tail.append(c)
                elif (die == 2):
                    honey_tail.append("")
                elif (die == 3):
                    honey_tail.append(special_ex[int(c)])
            elif c in special_ex:
                die = random.randint(0,3)
                if(die == 0):
                    honey_tail.append(random.choice(special_ex) )
                elif (die == 1):
                    honey_tail.append(c)
                    honey_tail.append(c)
                elif (die == 2):
                    honey_tail.append("")
                elif (die == 3):
                    idx = special_ex.find(c)
                    honey_tail.append(str(idx) if idx < 10 else c)
            elif c in string.ascii_lowercase:
                if(random.randint(0,1) == 0):
                    honey_tail.append(c.upper())
                else:
                    honey_tail.append(c)
            elif c in string.ascii_uppercase:
                if(random.randint(0,1) == 0):
                    honey_tail.append(c.lower())
                else:
                    honey_tail.append(c)
            else:
                honey_tail.append(random.choice(string.ascii_letters) )
        honey_list.append(''.join(honey_tail))
    return honey_list

def pwSeperate(s):
	list_isdigit = []
	for c in s:
		list_isdigit.append(c.isdigit())
	list_isdigit.append(not list_isdigit[-1])
	#print list_isdigit
	pw_seg = []
	pw_seg_isdigit = []
	start = 0
	for idx in range(0, len(list_isdigit) - 1):
		if list_isdigit[idx] ^ list_isdigit[idx+1]:
			pw_seg.append(s[start:idx+1])
			pw_seg_isdigit.append(s[start:idx+1].isdigit())
			start = idx+1
	#print pw_seg
	return pw_seg, pw_seg_isdigit	




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
        return [i.split() for i in f.readlines() if len(i.split()) == 2]

def read_input_file(filename):
    with open(filename) as f:
        return [i.strip() for i in f.readlines() if len(i.strip()) > 0]

### Password Generation ###

def generate_passwords(input_file, number=10):
    input_data = read_input_file(input_file)
    print len(input_data) 
    #sweetwords = [make_password(start, term, i, number) for i in input_data]
    return input_data

def get_honeywords(n, password, common_passwords):
    honeywords = [''] * int(n)
    if password in common_passwords:
        # then return n randomly chosen passwords
        #print 'password: ' , password
        for h in range(int(n)):
            w = password
            while(w == password):
                w = common_passwords[randint(0,len(common_passwords)-1)]    
            #print w   
            honeywords[h] = w
        return honeywords
    else:
        b = (nprand.permutation(gen(password, n/3, 5) + gen_digits(password, n/3) + gen_rand(password, n- n/3 -n/3))).tolist()
        return b


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


