import re

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
'.+\s='
'''
def test_filter_form1(line):
	rule='.+\s='
	return re.match(rule, line)

'''
form2:  python-idna >= 2.0  pkgconfig(gobject-2.0) >= 2.30
'.+\s>='
'''
def test_filter_form2(line):
	rule='.+\s>='
	return re.match(rule, line)

'''
form3:  perl(DateTime::Locale::kpe)  libQt53DLogic.so.5(Qt_5)
'.+\(.+\)'
note: form3 is depend of all-form1-form2
'''
def test_filter_form3(line):
	rule='.+\(.+\)'
	return re.match(rule, line)


def test_find_by_char(ch, l):
	ret=[]
	for d in list(l):
		m=re.match(ch, d)
		if m is not None:
			ret.append(d)
	return ret

l_conts_all = sorted(list(get_all_conts(r)))
l_deps_all  = sorted(list(get_all_deps(r)))
l_deps_form_1 = list( filter( test_filter_form1, l_deps_all ) )
l_deps_form_2 = list( filter( test_filter_form2, l_deps_all ) )
l_deps_form_3 = list( filter( test_filter_form3, (set(l_deps_all) - set(l_deps_form_1) - set(l_deps_form_2)) ) )

l_deps_char=[]
for i in range(26):
	l_deps_char.append(test_find_by_char( chr(i+ord('a') ), s_deps_all))


'''
fm1: 
xxx  { > < = >= <=}  yyy ==> xxx
'''
def filter_and_mod_1(line):
	r=line.split()
	if  len(r) == 3 :
		return r[0]
	else :
		return line

def fm1(s_deps_all):
	return sorted(list(set(list(map(filter_and_mod_1,s_deps_all)))))

'''
xxx  { > < = >= <=}  yyy ==> xxx
13319 -> 11713
'''
l_deps_all_filter_1 = fm1(l_deps_all)


'''
fm2: 
xxx(armv7hl-32)  ==>  xxx
'''
def filter_and_mod_2(line):
	m=re.search('\(armv7hl-32\)', line)
	if m is None:
		return line
	else:
		r=line.split('(')
		return r[0]

def fm2(l):
	return sorted(list(set(list(map(filter_and_mod_2, l)))))

l_deps_all_filter_1_2 = fm2(l_deps_all_filter_1)


def line_has_brackets(line):
	m=re.search('.+\(.+\)', line)
	if m is None :
		return False
	else:
		return True

l_deps_all_filter_1_2_has_brackets = list(filter( line_has_brackets, l_deps_all_filter_1_2))
l_deps_all_filter_1_2_no_brackets = list( set(l_deps_all_filter_1_2) - set(l_deps_all_filter_1_2_has_brackets))

def brackets_filter_special(line):
	m=re.match('pkgconfig\(|config\(|perl\(|font\(|mvn\(|ocaml\(|osgi\(|rpmlib\(|ruby\(|rubygem\(|php\(|tex\(|xserver-abi\(|rtld\(', line)
	if m is not None:
		return False
	m=re.search('\(armv7hl-32\)', line)
	if m is not None:
		return False	
	return True

l_brackets_no_special = list(filter( brackets_filter_special,l_deps_all_filter_1_2_has_brackets))

def brackets_get_body(l):
	ret=[]
	for line in l:
		r=line.split('(')
		ret.append(r[0])
	return sorted(list(set(ret)))

l_brackets_no_special_merged = brackets_get_body(l_brackets_no_special)   # (1) Just File



def brackets_get_pkgname(l):
	ret=[]
	for line in l:
		m = re.match('pkgconfig\(|config\(', line)
		if m is None:
			continue
		else:
			#print(line)
			r=line.split('(')
			ret.append(r[1][0:-1])
	return ret


l_brackets_get_packages = list(set(brackets_get_pkgname(l_deps_all_filter_1_2_has_brackets)) )   #(2) Pak name from config(xxx)  pkgconfig(xxx)



'''
Now use this function to filter all r[x][2]
'''
def filter_deps(deps):
	ret_fm1 = fm1(deps)
	ret_fm2 = fm2(ret_fm1)
	ret_has_brackets = list(filter( line_has_brackets, ret_fm2))
	ret_no_brackets = list( set(ret_fm2) - set(ret_has_brackets))
	ret_has_brackets_no_special = list(filter( brackets_filter_special,ret_has_brackets))
	ret_has_brackets_no_special_merged = brackets_get_body(ret_has_brackets_no_special)
	ret_has_brackets_get_packages = list(set(brackets_get_pkgname(ret_has_brackets)) )
	return set(ret_has_brackets_no_special_merged+ret_no_brackets+ret_has_brackets_get_packages)


all_deps_filtered = filter_deps(l_deps_all)


# Fixme: java-1.8.0-openjdk-1.8.0.161-2.b14.el7.armv7hl.rpm     mpich-3.0-3.0.4-10.el7.armv7hl.rpm
#
def get_pak_shot_name(long_name):
	m=re.match('.*?-[0-9]',long_name)
	if m is None:
		print(long_name)
		return None
	else:
		return m.group()[0:-2]

def foo(l):
	for line in l:
		r=line.split('.')
		sr=set(r)
		if ('el7' not in sr) and ('el7_0' not in sr) and ('el7_1' not in sr) and ('el7_2' not in sr) and ('el7_3' not in sr) and ('el7_4' not in sr) :
			print(line)


#  line.split('.el7')[0]

