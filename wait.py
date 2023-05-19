import threading
import time

wait_data = {}


def wait_count(num, name):
    count = int(num)
    count -= 1
    for i in range(int(num)):
        wait_data[name] = count
        count -= 1
        time.sleep(1)
        # print(wait_data[name])
    wait_data[name] = None


def wait(num, name):
    if name not in wait_data.keys():
        wait_data[name] = None
    wait_data[name] = int(num)
    threading.Thread(target=wait_count,args=(num,name,)).start()


def check(name):
    if name not in wait_data.keys():
        return None
    return wait_data[name]


"""example

wait.wait(60,"example")

if wait.check("example") is not None:
	return
    
"""
