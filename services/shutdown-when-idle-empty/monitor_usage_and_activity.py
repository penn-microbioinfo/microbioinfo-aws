import sys
from statistics import mean
from time import sleep
import re
import os
import subprocess
import datetime

cpuidlelog_path = '/var/shutdown-when-idle-empty'
free_out_pat = re.compile("^Mem[:][\s]+([0-9]+)[\s]+([0-9]+)[\s]+([0-9]+).+$")

def current_mem_usage():
    p = subprocess.Popen(["free", "-b"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out,err = p.communicate()
    if p.returncode != 0:
        raise OSError(err)
    else:
        out = out.decode("utf-8")
        for line in out.split('\n'):
            s = re.search(free_out_pat, line)
            if s is not None:
                total, used, free = s.groups()
                print(total, used, free)
                break

def current_cpu_idle():
    ps =subprocess.Popen(['bash', '/opt/shutdown-when-idle-empty/current_cpu_idle.bash'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out,err = ps.communicate()
    out_str = out.decode('utf-8').replace('\n', ',')[:-1]
    out_spl = [n for n in out_str.split(',')]
    return out_spl


def add_cpuidle_entry(cpuidlelog =cpuidlelog_path): 
    if os.path.isfile(cpuidlelog):
        os.remove(cpuidlelog)
    if os.path.isfile(cpuidlelog):
        fmode = 'a'
    else:
        fmode = 'w'

    with open(cpuidlelog, fmode) as hdl:
        now = current_cpu_idle()
        hdl.write('\t'.join(now))
        hdl.write('\n')
    return now

def get_mean_cpuidle(cpuidlelog =  cpuidlelog_path): 
    with open(cpuidlelog, 'r') as log:
        lines = [x.split('\t') for x in log.readlines()]
        cpu_avgs = []
        for cpuidx in range(0,len(lines[0])):
            core_entries = [float(x[cpuidx]) for x in lines]
            core_mean = mean(core_entries)
            cpu_avgs.append(core_mean)
    return cpu_avgs

def get_mean_cpuidle_diff(mean_idle_per_core, now):
        return mean([(m-n)/m for m,n in zip(mean_idle_per_core,now)])

def monitor():
    global last_10
    while True:
        if len(last_10) == 10:
            last_10 = last_10[1:]
        
        now = [float(n) for n in add_cpuidle_entry()]
        mean_idle_per_core = get_mean_cpuidle()
        last_10.append(mean(mean_idle_per_core))
        print(f"CPU Idle in current frame: {last_10}") 
        if len(last_10) == 10 and mean(last_10) > 85:
            return False
        else:
            return True

def parse_w_time(w_time):
    s = re.search('[a-z]$', w_time)
    if s is not None:
        endchar = s.group(0)
        if endchar == 's':
            seconds = re.sub('[.][0-9]{2}s$', '', w_time)
            time_in_seconds =int(seconds)
        elif endchar == 'm':
            spl = w_time.replace('m','').split(':')
            hours = spl[0]
            minutes = spl[1]
            time_in_seconds = int(hours)*3600 + int(minutes)*60
        else:
            raise ValueError('Unimplemented endchar {endchar}')
    else:
        spl = w_time.split(':')
        minutes = spl[0]
        seconds = spl[1]
        time_in_seconds = int(minutes)*60 + int(seconds)
    return(time_in_seconds)

def all_users_idle(w_out, time_limit=14400):
    user_idle_times = [parse_w_time(wo) for wo in w_out.split(',')]
    if any([wo<=time_limit for wo in user_idle_times]):
        active_user_idle_times =[wo for wo in user_idle_times if wo <= time_limit]
        print(f"There are {len(active_user_idle_times)} active users. Their idle times are (in seconds): {active_user_idle_times}")
        return False 
    else:
        return True

def are_there_active_users():
    ps = subprocess.Popen(['bash', '/opt/shutdown-when-idle-empty/check_active_users.bash'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    w_out,w_err = ps.communicate()
    w_out = w_out.decode('utf-8')
    if len(w_out) > 0:
        if all_users_idle(w_out=w_out):
            return False
        else:
            return True
    return False

def shutdown():
    subprocess.call(['shutdown', 'now'])

def run():
    while True:
        while monitor():
            sleep(360) 
        
        if not are_there_active_users():
            shutdown()
            break

        else:
            print(f"Wanted to shutdown based on CPU usage, but {active} users are logged in.") 

if __name__ == "__main__":
    last_10 = []
    run()
