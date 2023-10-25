progressBefore = 0
def printProgressBar(percent, prefix = ''):
    global progressBefore
    if percent - progressBefore < 0.001:	#只有当进度达到千分之一才刷新，避免频繁刷新进度条
        return
    progressBefore = percent
    percentStr = ("{0:.1f}").format(percent*100)
    filledLength = int(30 * percent)
    bar = '█' * filledLength + '-' * (30 - filledLength)
    print('\r%s |%s| %s%% ' % (prefix, bar, percentStr),end='')

if __name__ == "__main__":
    import time
    for i in range(1000):
        printProgressBar((i+1)/1000,prefix="Progress:")
        time.sleep(0.01)		#当前进程暂停10ms