 
import subprocess
import os
import pickle


'''
return {'rpmname':[f1, f2...]}
subprocess.check_output("ls").decode('utf-8').splitlines()
subprocess.check_output(["ls",'-l' ]).decode('utf-8').splitlines()
'''
def get_rpm_contents(rpmname):
	cmd="rpm -qpl %s" %(rpmname)
	ret=subprocess.check_output(cmd.split(' ')).decode('utf8').splitlines()
	return {rpmname: ret}

def get_rpm_deps(rpmname):
	cmd="rpm -qpR %s" %(rpmname)
	ret=subprocess.check_output(cmd.split(' ')).decode('utf8').splitlines()
	return {rpmname: ret}

def process_whole_mirror(path):
	conts=[]
	deps=[]
	for f in os.listdir(path):
		abs_fn=path+"/"+f
		try:
			conts.append(get_rpm_contents(abs_fn))
			deps.append(get_rpm_deps(abs_fn))
		except:
			print("===error :%s ===" %(abs_fn))
	return conts, deps

def save_conts_deps(fn,conts,deps):
	f=open(fn,"wb")
	pickle.dump((conts,deps), f)
	f.close()

def load_conts_deps(fn):
	f=open(fn,"rb")
	c=pickle.load(f)
	return c[0], c[1]

def save_conts_deps_for_whole_mirror(fn, mirror_path):
	conts, deps = process_whole_mirror(mirror_path)
	save_conts_deps(fn, conts, deps)






