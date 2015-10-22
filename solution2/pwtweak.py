import string
import random
import sys
import csv
from datetime import date
import numpy.random as nprand

def gen_tail(pw, t):
	special_ex = '[~!@#$%^&*()_+{}":;\\\']+$'
	if t > len(pw):
		t = len(pw)
		
	honey_tail = []
	for c in pw[-t:]:
		if c.isdigit():
			honey_tail.append(random.choice(string.digits) )
		elif c in special_ex:
			honey_tail.append(random.choice(special_ex) )
		else:
			if random.random() < 0.3:
				honey_tail.append(random.choice(string.ascii_letters) )
			else:
				honey_tail.append(c)
	return pw[:len(pw)- t]+''.join(honey_tail)
		

def gen_digits(pw):
	pw_seg, pw_seg_isdigit = pwSeperate(pw)
	pw_seg_cp = list(pw_seg)
	idx_list = []
	for idx, isdigit in enumerate(pw_seg_isdigit):
		if isdigit :
			idx_list.append(idx)

	for idx in idx_list:
		seg = pw_seg[idx]
		if len(seg)==1 or len(seg) > len(pw) * 0.8:
			pw_seg_cp[idx] = seg
		elif (len(seg)==4 and ((seg[0:2] == "19") or (seg[0:2] == "20")) ):
			pw_seg_cp[idx] = str(random.choice(range(1900, date.today().year)))
		else:
			randnu = random.randint(0, 10**(len(seg) + random.randint(0, 1)) - 1)
			pw_seg_cp[idx] = str(randnu)
	return ''.join(pw_seg_cp)

def gen_rand(pw):
	special_ex = ')!@#$%^&*([~_+{}":;\\\']+$'

	honey_tail = []
	for c in pw:
		if c.isdigit():
			if(random.random() < 0.8):
				honey_tail.append(c)
			elif (random.random() < 0.3):
				honey_tail.append(c)
				honey_tail.append(c)
			elif (random.random() < 0.8):
				honey_tail.append("")
			else:
				honey_tail.append(special_ex[int(c)])
		elif c in special_ex:
			if(random.random() < 0.8):
				honey_tail.append(c)
			elif (random.random() < 0.3):
				honey_tail.append(c)
				honey_tail.append(c)
			elif (random.random() < 0.8):
				honey_tail.append("")
			else:
				idx = special_ex.find(c)
				honey_tail.append(str(idx) if idx < 10 else c)
		elif c in string.ascii_lowercase:
			if (random.random() < 0.4):
				honey_tail.append(c.upper())
			else:
				honey_tail.append(c)
		elif c in string.ascii_uppercase:
			if (random.random() < 0.4):
				honey_tail.append(c.lower())
			else:
				honey_tail.append(c)
		else:
			honey_tail.append(c)
	return ''.join(honey_tail)

def gen_leet(pw):

	leetDict = {"a": "@", "@": "a", "s": "$","$":"s" ,"e": "3","3": "e", "t": "7", "7": "t", "o": "0","0": "o" ,"i": "|", "|": "i", "1": "l", "l": "1"}
	hw = ""
	count = 0

	# find the number of eligible chars
	for c in pw:
		if c.lower() in leetDict:
			count += 1

	for c in pw:
		if not c.lower() in leetDict:
			hw += c
			continue

		if random.random() < 0.4 and random.random() < 2.0 / count:
			if random.random() < 0.5:
				hw += leetDict[c.lower()]
			else:
				hw += leetDict[c.lower()].upper()
		else:
			hw += c

	return hw

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

def gen_honeyword(pw):
	hw = pw
	hw = gen_leet(hw)
	hw = gen_digits(hw)
	hw = gen_rand(hw)
	hw = gen_leet(hw)
	print hw
	# ensures that every time, the same proportion of honeywords are all lowercase
	return hw



def password_gen(input_f, n):
	if n <= 1:
		print "n need to be >= 2"
		sys.exit(1)

	pw_list = read_input_file(input_f)
	sweetlist = []
	for pw in pw_list:
		honeylist = [pw]
		for i in range(0, n):
			honeylist += [gen_honeyword(pw)]
		sweetlist.append(nprand.permutation(honeylist))
	return sweetlist

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
	#print sweetwords
	write_csv(argv[3], sweetwords)

if __name__ == "__main__":
	main(sys.argv)
