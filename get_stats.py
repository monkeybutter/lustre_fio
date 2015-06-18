import json
import subprocess

gdatas = [1, 2]
lustre_stripes = [1, 2, 4, 8]
cpu_nodes = [0, 1]
mem_binds = [0, 1]
thread_ns = [2, 4, 8]
readwrites = ["read", "write"]

def remove_dot_key(obj):
    for key in obj.keys():
        new_key = key.replace(".","d")
        if new_key != key:
            obj[new_key] = obj[key]
            del obj[key]
    return obj

json_list = []

for gdata in gdatas:
    for lustre_stripe in lustre_stripes:
        for cpu_node in cpu_nodes:
            for mem_bind in mem_binds:
                for readwrite in readwrites:
                    for thread_n in thread_ns:
            
                        command = ["numactl", "--cpunodebind={}".format(cpu_node), "--membind={}".format(mem_bind),
                           "/home/900/prl900/fio/fio", "--randrepeat=0", "--ioengine=libaio", "--directory=/g/data{}/z00/prl900/HPData{}".format(gdata, lustre_stripe), 
                           "--name=cpub{}_memb{}_gdata{}_ls{}_{}_th{}".format(cpu_node, mem_bind, gdata, lustre_stripe, readwrite, thread_n), 
                           "--filename=test", "--bs=1024k", "--iodepth=8", "--thread", "--numjobs={}".format(thread_n), "--size=1G", "--readwrite={}".format(readwrite),
                           "--output-format=json"]
            
                        json_list.append(json.loads(subprocess.check_output(command), object_hook=remove_dot_key))
            
with open("/home/900/prl900/profiler/fio_output.json", "w") as f:
    json.dump(json_list, f) 
