import string
import random
import sys
import csv
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
				honey_tail.append(random.choice(special) )
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
                    idx = special.find(c)
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
def read_input_file(filename):
    with open(filename) as f:
        return [i.strip() for i in f.readlines() if len(i.strip()) > 0]
def write_csv(filename, values):
    with open(filename, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(values)
def password_gen(input_f, n):
	pw_list = read_input_file(input_f)
        
        return [ nprand.permutation(gen(pw, n/3, 5) + gen_digits(pw, n/3) + gen_rand(pw, n- n/3 -n/3)) for pw in pw_list]

def main(argv):
    if len(sys.argv) != 4:
        print "Generate the honeywords."
        print ""
        print "python solution3.py n inputfile outputfile"
        print ""
        print "     n               the number of passwords"
        print "     inputfile       the filename of inputfile"
        print "     outputfile      the filename of outputfile"
        sys.exit(1)
    sweetwords = password_gen(argv[2], int(argv[1]))
    write_csv(argv[3], sweetwords)

if __name__ == "__main__":
    main(sys.argv)
