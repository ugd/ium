import multiprocessing, time, signal
p = multiprocessing.Process(target=time.sleep, args=(5000,))
print(p, p.is_alive())
p.start()
print(p, p.is_alive())
p.terminate()
time.sleep(3)
print(p, p.is_alive())
p.exitcode == -signal.SIGTERM
