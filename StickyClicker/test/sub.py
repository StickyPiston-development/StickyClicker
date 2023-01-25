import subprocess, time

process = subprocess.Popen("python StickyClicker/stickyclicker.py", shell=True)
time.sleep(5)
subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=process.pid))