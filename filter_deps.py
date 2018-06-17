 import re

def filter_deps():
	pass


'''
r:=
[
[ 'rpmname', [contents], [deps]]
....
]
'''

'''
get_all_deps: collect all deps in a set
r: is metadata
'''
def get_all_deps(r):
	ss=set()
	for item in r:
		for sub_item in item[2]:
			ss.add(sub_item)
	return ss

'''
get_all_conts: collect all conts in a set
r: is metadata
'''
def get_all_conts(r):
	ss=set()
	for item in r:
		for sub_item in item[1]:
			ss.add(sub_item)
	return ss


'''
form1:  libqb = 1.0.1-6.el7 , libcroco(armv7hl-32) = 0.6.11-1.el7
form2:  ORBit2 >= 2.6.0  
form3:  pkgconfig(Qt5Test)  
'''

'''
form1:  libqb = 1.0.1-6.el7 , libcroco(armv7hl-32) = 0.6.11-1.el7
'.+\s='
'''
def filter_form1(line):
	rule='.+\s='
	return re.match(rule, line)

def filter_not_form1(line):
	rule='.+\s='
	return not re.match(rule, line)


'''
form2:  python-idna >= 2.0  pkgconfig(gobject-2.0) >= 2.30
'.+\s>='
'''
def filter_form2(line):
	rule='.+\s>='
	return re.match(rule, line)

def filter_not_form2(line):
	rule='.+\s>='
	return not re.match(rule, line)


'''
form3:  perl(DateTime::Locale::kpe)  libQt53DLogic.so.5(Qt_5)
'.+(.+)'
note: form3 is depend of all-form1-form2
'''
def filter_form3(line):
	rule='.+\(.+\)'
	return re.match(rule, line)

def filter_not_form3(line):
	rule='.+\(.+\)'
	return not re.match(rule, line)


'''
form4:  rpmlib(CompressedFileNames) <= 3.0.4-1
'rpmlib\(.*\)'
note: form3 is depend of all-form1-form2
'''	
def filter_form4(line):
	rule='rpmlib\(.*\)'
	return re.match(rule, line)

def filter_not_form4(line):
	rule='rpmlib\(.*\)'
	return not re.match(rule, line)






'''
libFLAC++.so.6		==>  '++' will lead exception
/usr/bin/[			==>  '['  will lead exception
'''
def find_all_invaild_deps():
	ret=[]
	conts=list(s_conts_all)[0:5]
	for d in list(s_deps_remained):
		for c in conts:
			try :
				m=re.match(d,c)
			except:
				ret.append(d)
				print(d)
				break
	return ret

'''
libFLAC++.so.6
dvd+rw-tools
'''
def find_all_plus():
	ret=[]
	for d in list(s_deps_remained):
		m=re.search('\+', d)
		if m is not None:
			print(d)
			ret.append(d)
	return ret

'''
+ . * [ ] ( )
'''	
def find_all_meta_char():
	ret=[]
	for d in list(s_deps_remained):
		m=re.search('[\.\*\+\[\]\(\)]', d)
		if m is not None:
			ret.append(d)
	return ret


def find_by_char(ch, l):
	ret=[]
	for d in list(l):
		m=re.match(ch, d)
		if m is not None:
			ret.append(d)
	return ret

s_conts_all = get_all_conts(r)
s_deps_all = get_all_deps(r)
l_deps_form_1 = list( filter( filter_form1, s_deps_all ) )
l_deps_form_2 = list( filter( filter_form2, s_deps_all ) )
l_deps_form_3 = list( filter( filter_form3, (s_deps_all - set(l_deps_form_1) - set(l_deps_form_2)) ) )
s_deps_remained = s_deps_all - set(l_deps_form_1) - set(l_deps_form_2) - set(l_deps_form_3)

l_deps_char=[]
for i in range(26):
	l_deps_char.append(find_by_char( chr(i+ord('a') ), s_deps_all))

