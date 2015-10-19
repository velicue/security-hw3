import string
import random
import sys
import csv

def gen(pw, k, t):
    char = 1
    no = 2
    special = 3
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
		

def gen_digits(pw, k, t):
	char = 1
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
	return [gen(pw, n, 3) for pw in pw_list]

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
