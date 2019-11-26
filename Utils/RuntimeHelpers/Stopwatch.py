import time
startTime = 0
stopTime = 0
def start():
    global startTime
    startTime = time.time()

def stop():
    stopTime = time.time()
    global startTime
    #print(f"{startTime} , {stopTime}, {startTime - stopTime}")
    if stopTime - startTime > 0:
        return "{:8.2f}".format(1 / ( stopTime - startTime )) + " Hz"
    else:
        return 'InfinitePow'
def sleep(t):
    time.sleep(t)