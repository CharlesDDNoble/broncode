import plotly.graph_objects as PGraph
import plotly.io as PIO
import plotly.express as PExpress

import matplotlib.pyplot as plt

from testobject import Trial, Test

def log_test(test_name,test,file_name="test_data.log",should_append=True):
    if should_append:
        mode = "a"
    else:
        mode = "w"
    with open(file_name,mode) as f:
        # print(test_name+"\n")
        f.write((test.to_json())+"\n")


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

    if None in test:
        print("WARNING: The test list has an index with None!")
    
    if is_random:
        print("Random Seed used: "+str(seed))

    print("TOTALS")
    print_stats(test)
    
    if passes:
        print("PASSES")
        print("\tPasses/Total:                  "+str(len(passes))+"/"+str(len(test)))
        print_stats(passes)

    else:
        print("WARNING: NO PASSING TESTS")

    if fails:
        print("FAILS")
        print("\tFails/Total:                   "+str(len(fails))+"/"+str(len(test)))
        print_stats(fails)
    else:
        print("NO FAILING TESTS")

    print("=============================================================")

    log_data(test_name,test)

def create_scat_plot(test_name,tests,xlab='',ylab='',log_name="student_simuations.log"):
    x_data = []
    y_data = []
    max_x = 10

    for test in tests:
        log_test(test.name,test,log_name,should_append=True)
        if len(test.trials):
            # fails = filter(is_failing,test.data)
            x_data += [test.count]
            y_data += [test.get_success_rate()]
            max_x = max(max_x,test.count)
        else:
            print(test.to_dict())
            print("WARNING: Found test with no data!")

    #So the index is not on edge of graph
    max_x += max_x/5

    plt.plot(x_data, y_data, 'ro')
    #[xmin,xmax,ymin,ymax]
    plt.axis([0, max_x, 0, 1.05])
    plt.title(test_name)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.show()
    plt.saveFig("30_replica_student_test.png")

# PLOTLY
# def create_scat_plot(test_name,tests,xlab='',ylab=''):
#     x_data = []
#     y_data = []
#     max_x = 10

#     for test in tests:
#         log_data(test.name,test,"student_simuations.log",should_append=True)
#         if len(test.trials):
#             # fails = filter(is_failing,test.data)
#             x_data += [test.count]
#             y_data += [test.get_success_rate()]
#             max_x = max(max_x,test.count)
#         else:
#             print(test.to_dict())
#             print("WARNING: Found test with no data!")

#     #So the index is not on edge of graph
#     max_x += max_x/5

#     fig = PExpress.scatter(x=x_data,
#                         y=y_data,
#                         labels={'x':xlab,'y':ylab},
#                         range_y=[0,1.05],
#                         range_x=[0,max_x])
#     fig.write_image("report_1.png")
#     pio.write_html(fig, file='report_1.html', auto_open=True)
#     fig.show()
