import string
import random

def gen(pw, k, t):
	char = 1
	no = 2
	special = 3
	special_ex = '[~!@#$%^&*()_+{}":;\\\']+$'
	if t > len(pw):
		t = len(pw)
	honey_list = []
	for k in range(0,k):
		hoeny_tail = []
		for c in pw[-t:]:
			if c.isdigit():
				honey_tail.append(random.choice(string.digits) )
			elif c in special_ex:
				honey_tail.append(random.choice(special) )
			else:
				honey_tail.append(random.choice(string.ascii_letters) )
		honey_list.append(pw[:len(pw)- t]+''.join(honey_tail))
	print honey_list
		

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
		
