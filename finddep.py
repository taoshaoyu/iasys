 
import subprocess
import os
import pickle


'''
[
{"rpmname":([contents], [deps])}
]
'''

def process_rpm(mirror_path, rpm_fn):
	cmd="rpm -qpl %s" %(mirror_path+'/'+rpm_fn)
	conts=subprocess.check_output(cmd.split(' ')).decode('utf8').splitlines()
	cmd="rpm -qpR %s" %(mirror_path+'/'+rpm_fn)
	deps=subprocess.check_output(cmd.split(' ')).decode('utf8').splitlines()
	return [rpm_fn,conts, deps]

def process_rpms(mirror_path):
	ret=[]
	for fn in os.listdir(mirror_path):
		try:
			r=process_rpm(mirror_path, fn)
			ret.append(r)
		except:
			print("===error :%s ===" %(mirror_path+'/'+fn))
			continue		
	return ret

def save_result(fn,ret):
	f=open(fn,"wb")
	pickle.dump(ret, f)
	f.close()

def save_conts_deps_for_whole_mirror(fn, mirror_path):
	ret = process_rpms(mirror_path)
	save_result(fn, ret)

def load_conts_deps(fn):
	f=open(fn,"rb")
	return pickle.load(f)







