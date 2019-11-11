import matplotlib.pyplot as plt

from testobject import Trial, Test

def is_passing(trial):
    return trial.is_success

def is_failing(trial):
    return not trial.is_success

def print_stats(trials):
    sum_test_time = sum(trial.test_time for trial in trials)
    sum_run_time = sum(trial.test_time for trial in trials)
    count = len(trials)
    print("\tTotal test time:               "+str(sum_test_time))
    print("\tTotal connection and run time: "+str(sum_run_time))
    print("\tAvg. time of request:          "+str(sum_test_time/count))
    print("\tAvg. time to connect and run:  "+str(sum_run_time/count))

def print_report(test,is_random=False,seed=0):
    passes = list(filter(is_passing,test.trials))
    fails = list(filter(is_failing,test.trials))

    print("=============================================================")
    print(test.name+" Test Report:")

    if None in test.trials:
        print("WARNING: The Test.trials contains indexes with None!")
    
    if is_random:
        print("Random Seed used: "+str(seed))

    print("TOTALS")
    print_stats(test.trials)
    
    if passes:
        print("PASSES")
        print("\tPasses/Total:                  "+str(len(passes))+"/"+str(len(test.trials)))
        print_stats(passes)
    else:
        print("WARNING: NO PASSING TESTS")

    if fails:
        print("FAILS")
        print("\tFails/Total:                   "+str(len(fails))+"/"+str(len(test.trials)))
        print_stats(fails)
    else:
        print("NO FAILING TESTS")

    print("=============================================================")


def get_percent_success_vs_count(tests):
    xdata = []
    ydata = []
    max_x = 10

    for test in tests:
        if len(test.trials):
            # fails = filter(is_failing,test.data)
            xdata += [test.count]
            ydata += [test.get_success_rate()]
            max_x = max(max_x,test.count)
        else:
            print(test.to_dict())
            print("WARNING: Found test with no data!")

    #So the index is not on edge of graph
    max_x += max_x/5
    axis = [0,max_x,0,1.05]
    return (xdata,ydata,axis)

def scatter(test_name,xdata,ydata,axis,xlab='',ylab='',save_format=".png"):
    plt.plot(xdata, ydata, 'ro')
    #[xmin,xmax,ymin,ymax]
    plt.axis(axis)
    plt.title(test_name)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    # vvv This must happen before plt.show() vvv
    plt.savefig(test_name+save_format)
    plt.show()
