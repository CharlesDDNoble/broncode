import subprocess
import math
import random
from os import path
from copy import deepcopy
from threading import Thread, Timer
from time import time, sleep
import json

from codeclient import CodeClient
import plotly.graph_objects as PGraph

host = ''
port = 4000
flags = " -o3 \n" 

bad_code =  "int main(int argc,char** argv){error;return 0;}\n"
bad_exp  =  "Parsing gcc flags...\n" \
            "Compiling code...\n" \
            "gcc -o3 -o code code.c\n" \
            "Something went wrong compiling your code:\n" \
            "code.c: In function 'main':\n" \
            "code.c:1:32: error: 'error' undeclared (first use in this function)\n" \
            " int main(int argc,char** argv){error;return 0;}\n" \
            "                                ^~~~~\n" \
            "code.c:1:32: note: each undeclared identifier is reported only once for each function it appears in\n"

good_code = "int main(int argc,char** argv){printf(\"Hello!\\n\");return 0;}\n"
good_exp  = "Parsing gcc flags...\n" \
            "Compiling code...\n" \
            "gcc -o3 -o code code.c\n" \
            "Executing program...\n" \
            "./code\n" \
            "Your code successfully compiled and ran, here's the output:\n" \
            "Hello!\n"

inf_code =  "int main(int argc,char** argv){while(1);return 0;}\n"
inf_exp  =  "Something went wrong running your code:\n" \
            "It took too long to execute, so we stopped it!\n"

inputs = [  (bad_code,bad_exp),
            (good_code,good_exp),
            (inf_code,inf_exp)  ]

class TestData():

    def to_dict(self):
        return {"is_success" : self.is_success,
                "test_time" : self.test_time,
                "out" : self.out,
                "exp" : self.exp,
                "handler" : self.handler.to_dict(),
                "failure_reason" : self.failure_reason}


    def __init__(self,test_time,out,exp,handler):
        self.is_success = (out == exp)
        self.test_time = test_time
        self.out = out
        self.exp = exp
        self.handler = handler
        if self.is_success:
            self.failure_reason = "none"
        elif self.out == inf_exp:
            self.failure_reason = "timeout"
        else:
            self.failure_reason = "wrong"

    def print(self):
        print("is_success: "+str(self.is_success))
        print("test_time: "+str(self.test_time))
        print("out: "+self.out.replace("\n","\\n"))
        print("exp: "+self.exp.replace("\n","\\n"))
        print("handler: "+str(self.handler))

    def get_data_string(self):
        return  str(self.is_success) + "," \
                + str(self.test_time) + "," \
                + str("\'"+self.out.replace("\n","\\n")+"\'") + "," \
                + str("\'"+self.exp.replace("\n","\\n")+"\'") + "," \
                + str(self.failure_reason) + "," \
                + str(self.handler.run_time) + "," \
                + str(self.handler.send_time) + "," \
                + str(self.handler.recv_time) + "," \
                + str(self.handler.conn_attempt)

class Test():

    def __init__(self,name,test_type,count,interval,time_limit,data = []):
        self.name = name
        self.test_type = test_type
        self.count = count
        self.interval = interval
        self.time_limit = time_limit
        self.data = data


def log_data(test_name,test,file_name="test_data.log",should_append=True):
    if should_append:
        mode = "a"
    else:
        mode = "w"
    with open(file_name,mode) as f:
        print(test_name+"\n")
        for data in test:
            json.dump
            f.write(json.dumps(data.to_dict())+"\n")


def is_passing(test):
    return test.is_success

def is_failing(test):
    return not test.is_success

def print_stats(all_data):
    sum_test_time = sum(data.test_time for data in all_data)
    sum_run_time = sum(data.test_time for data in all_data)
    count = len(all_data)
    print("\tTotal test time:               "+str(sum_test_time))
    print("\tTotal connection and run time: "+str(sum_run_time))
    print("\tAvg. time of request:          "+str(sum_test_time/count))
    print("\tAvg. time to connect and run:  "+str(sum_run_time/count))

def print_report(test,is_random=False,seed=0):
    passes = list(filter(is_passing,test))
    fails = list(filter(is_failing,test))

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

def make_student_scatter_plot(test_name,tests):
    x = []
    y = []
    for test in tests:
        count = len(test)


    fig = PGraph.Figure({
        "data": [{"type": "scatter",
                  "x": x,
                  "y": y}],
        "layout": {
            "title": {"text": "Student Simulation with 20 sec Max Wait"},
            "xaxis": {
                "title": {"text": "Number of Students"},
                "range": [0,100]
            },
            "yaxis": {
                "title": {"text": "Percent of Executions with Runtime < 8 Sec "},
                "range": [0,100]
            },
        }
    })

# returns a TestData object corresponding to the results of the trial
def execute_request(code,exp,trials,index,wait=0):
    sleep(wait)

    test_time = time()

    host = ''
    port = 4000
    flags = " -o3 \n" 
    
    handler = CodeClient(host,port,code,flags)
    handler.run()
    

    out = handler.log.replace('‘','\'').replace('’','\'')

    test_time = time() - test_time

    data = TestData(test_time,out,exp,handler)


    trials[index] = data


def has_max_replicas(service_name):
    command = ["docker", "service", "ls", "--filter", "name="+service_name, "--format", "{{.Replicas}}"]
    done_process = subprocess.run(command, 
                        stdout = subprocess.PIPE, 
                        stderr = subprocess.PIPE)
    out = done_process.stdout.decode("utf-8").split("/")
    err = done_process.stderr.decode("utf-8")

    count = int(out[0])
    total = int(out[1])

    if err:
        return False

    return (count == total)

def run_test(service_name,test_name,code,exp,total,interval,should_print=False):
    while not has_max_replicas(service_name):
        sleep(1)

    trials = [None] * total

    for i in range(total):
        execute_request(code,exp,trials,i,interval)

    test = Test(test_name,"Single-Thread",total,interval,interval,trials)

    if should_print and trials:
        print_report(test)
    elif not trials:
        print("No test data collected")

    return test

def run_threaded_test(service_name,test_name,code,exp,total,interval,is_random=False,should_print=False):
    while not has_max_replicas(service_name):
        sleep(1)

    seed = math.floor(time())
    random.seed(seed)

    trials = [None] * total
    threads = [None] * total

    for i in range(total):
        # assign a wait time based on the given interval for the thread to wait before execution
        if is_random:
            wait = random.random() * interval
        else:
            wait = interval * i

        thread = Thread(target=execute_request,args=(code,exp,trials,i,wait))
        threads[i] = thread

    for i in range(total):
        threads[i].start()

    # assign a wait time for each thread to finish. Assuming that the execution of
    # the thread itself is (its wait time + 10), the +10 is for connecting and running.
    if is_random:
        wait = interval + 10
    else:
        wait = interval * total + 10


    for i in range(total):
        threads[i].join(wait)

    test = Test(test_name,"Multi-Thread",total,interval,interval,trials)
 
    if should_print and trials:
        print_report(test,is_random,seed)
    elif not trials:
        print("No test data collected")

    return test

def simulate_student(trials,index,time_limit,max_wait):
    start_time = time()
    
    random.seed(start_time)
    
    next_execution = random.random() * max_wait

    my_trials = []
    count = 0

    while time() - start_time < time_limit:
        if next_execution <= 0:
            inp = math.floor(random.random() * len(inputs))
            code, exp = inputs[inp]
            my_trials += [None]
            execute_request(code, exp, my_trials, count)
            count += 1
            next_execution = 5 + random.random() * max_wait
        else:
            next_execution -= 1
            sleep(1)

    trials[index] = my_trials

def run_student_test(service_name,test_name,student_count,time_limit,max_wait,should_print=False):
    while not has_max_replicas(service_name):
        sleep(1)

    trials = [None] * student_count
    threads = [None] * student_count

    for i in range(student_count):
        threads[i] = Thread(target=simulate_student,args=(tests,i,time_limit,max_wait))
        threads[i].start()

    for i in range(student_count):
        threads[i].join(time_limit + 10)

    collected_trials = []

    for i in range(student_count):
        if trials[i]:
            collected_trials += trials[i]

    test = Test(test_name,"Student",total,time_limit,max_wait,collected_trials)

    if should_print and collected_trials:
        print_report(test_name,test)
    elif not collected_trials:
        print("WARNING: No test data collected")

    return test

def prepare_percentile_data(tests):
    data = [[0] * 2]
    for test in tests:
        count = len(tests)
        passes = len(list(filter(is_passing,tests)))

def main():
    service_name = "broncode_c_service"
    reps = 60

    # ======================== NON THREADED TESTS ========================
    # Every INTERVAL seconds, send code to the given service for compiling and running.
    # Repeat the process REPS times.

    # BAD CODE
    # code, exp = inputs[0]

    # run_tests(service_name,"Bad Code 5-interval",code,exp,reps,5)

    # # GOOD CODE
    # code, exp = inputs[1]

    # run_tests(service_name,"Good Code 5-interval",code,exp,reps,5)

    # # INF CODE
    # code, exp = inputs[2]
    
    # run_tests(service_name,"Infinite Code 5-interval",code,exp,reps,5)

    # ======================== THREADED TESTS - Regular Interval ========================
    # Start a thread every INTERVAL seconds that sends code to the given service for 
    # compiling and running. Repeat the process REPS times.

    # BAD CODE
    # code, exp = inputs[0]

    # run_threaded_tests(service_name,"Bad Code Threaded 5-interval",code,exp,reps,5)

    # # GOOD CODE
    # code, exp = inputs[1]

    # run_threaded_tests(service_name,"Good Code Threaded 5-interval",code,exp,reps,5)

    # # INF CODE
    # code, exp = inputs[0]

    # run_threaded_tests(service_name,"Infinite Code Threaded 5-interval",code,exp,reps,5)

    # ======================== THREADED TESTS - Random Interval ========================
    # Start a REPS threads and assign a random wait time within INTERVAL for the thread
    # to begin execution, namely sending a code to the given service for compiling and running.

    # BAD CODE
    # code, exp = inputs[0]

    # run_threaded_tests(service_name,"Bad Code Threaded Random 180-interval 60-Repitions",code,exp,reps,180,True)

    # # GOOD CODE
    # code, exp = inputs[1]

    # run_threaded_tests(service_name,"Good Code Threaded Random 30-interval",code,exp,reps,30,True)

    # # INF CODE
    # code, exp = inputs[0]

    # run_threaded_tests(service_name,"Infinite Code Threaded Random 30-interval",code,exp,reps,30,True)

    # ======================== SIMULATED STUDENT TESTS ========================

    sim_tests = []

    data = run_student_test(service_name,"Simulated Student Test 10-limit",30,10,10)
    sim_tests += Test("Simulated 10-Student Test 10-limit 10-wait",10,10,10,data)

    data = run_student_test(service_name,"Simulated Student Test 10-limit",30,10,10)
    sim_tests += Test("Simulated 20-Student Test 10-limit 10-wait",20,10,10,data)
    
    data = run_student_test(service_name,"Simulated Student Test 10-limit",30,10,10)
    sim_tests += Test("Simulated 30-Student Test 10-limit 10-wait",30,10,10,data)

    print_report("Simulated Student Tests",sim_tests)





if __name__ == "__main__":
    main()