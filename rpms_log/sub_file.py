'''
sub_file:
sub_file f1 f2
context of f1 - f2
'''
import sys
fn1=sys.argv[1]
fn2=sys.argv[2]

def get_fl(fn):
	f=open(fn)
	lf=f.readlines()
	r=[]
	for line in lf:
		r.append(line.strip())
	rs=set(r)
	return rs

s1=get_fl(fn1)
s2=get_fl(fn2)

for i in (s1-s2): 
	print (i)