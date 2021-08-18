import subprocess
import time
from datetime import datetime
import sys
import platform

current_os = platform.system()

def get_cpu_usage(pid):
  cmd = ["top", "-p", str(pid), "n1", "b"]
  x = subprocess.run(cmd, capture_output=True)
  output = x.stdout.decode()
  return output

def is_gpu_available():
  cmd = ["nvidia-smi"]
  x = subprocess.run(cmd, capture_output=True)
  return x.returncode == 0

def get_gpu_memory():
  cmd = ['nvidia-smi', '--query-gpu=memory.used,utilization.gpu', '--format=csv']
  x = subprocess.run(cmd, capture_output=True)
  output = x.stdout.decode()
  output_values = output.split("\n")
  used_memory = output_values[1].split(",")[0]
  utilization = output_values[1].split(",")[1]
  return used_memory, utilization

pid = input("Enter a process id: ")

gpu_available = is_gpu_available()
if gpu_available:
  print("GPU Found")
else:
  print("GPU not Found")

log_file = "log.txt"

while True:

  sys.stdout = open(log_file, 'a+')

  if current_os != "Windows":
    usage = get_cpu_usage(pid)
    usage_lines = usage.split("\n")
    usage_separated = usage_lines[7].split()
    pid_no = usage_separated[0]
    pid_cpu = usage_separated[8]
    pid_mem = usage_separated[9]
    datetime_obj = datetime.now()
    print("PID: {}, CPU: {}, MEM: {}, DATE: {}".format(pid_no, pid_cpu, pid_mem, datetime_obj))
  
  if gpu_available:
    gpu_used_memory, gpu_utilization = get_gpu_memory()
    print("GPU used: {}, GPU Utilization: {}".format(gpu_used_memory, gpu_utilization))
  
  
  time.sleep(5)
  