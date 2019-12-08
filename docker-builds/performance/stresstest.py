import subprocess
import math
import random
from os import path
from copy import deepcopy
from threading import Thread, Timer
from time import time, sleep

import visualizer
from testobject import Trial, Test
from codeclient import CodeClient

#TODO: Implement functionality to associate service_name to correct docker service
#      I input service name (and maybe host/port), and the tests are run for that service

# Hack: This is assigned in main, giving it global scope due to my own laziness
timeout_response = ""

# returns a Trial object corresponding to the results of the trial
def execute_request(code,exp,trials,index,wait=0):
    sleep(wait)

    test_time = time()

    host = ''
    port = 4000
    flags = " -O3 \n" 
    
    handler = CodeClient(host,port,code,flags)
    handler.run()
    

    out = handler.log.replace('‘','\'').replace('’','\'')

    test_time = time() - test_time

    trial = Trial(test_time,out,exp,timeout_response,handler)

    trials[index] = trial

# check that the service is at its maximum number of replicas
def has_max_replicas(service_name):
    command = ["docker", "service", "ls", "--filter", "name="+service_name, "--format", "{{.Replicas}}"]
    done_process = subprocess.run(command, 
                        stdout = subprocess.PIPE, 
                        stderr = subprocess.PIPE)
    out = done_process.stdout.decode("utf-8").split("/")
    err = done_process.stderr.decode("utf-8")
    try:
        count = int(out[0])
        total = int(out[1])

        if err:
            return True
    except Exception as ex:
        print(ex)
        print("This may be a permission issue. Try running with sudo.")
        raise SystemExit

    return (count == total)

# ======================== NON THREADED TESTS ========================
# Every INTERVAL seconds, send code to the given service for compiling and running.
# Repeat the process REPS times.

def run_test(service_name,test_name,code,exp,total,interval):
    while not has_max_replicas(service_name):
        sleep(.1)

    trials = [None] * total

    for i in range(total):
        execute_request(code,exp,trials,i,interval)

    test = Test(test_name,"Single-Thread",total,interval,interval,trials)

    return test

# ======================== THREADED TESTS - Regular Interval ========================
# Start a thread every INTERVAL seconds that sends code to the given service for 
# compiling and running. Repeat the process REPS times.

# ======================== THREADED TESTS - Random Interval ========================
# Start a REPS threads and assign a random wait time within INTERVAL for the thread
# to begin execution, namely sending a code to the given service for compiling and running.

def run_threaded_test(service_name,test_name,code,exp,total,interval,is_random=False):
    while not has_max_replicas(service_name):
        sleep(.1)

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

    return test

def simulate_student(trials,index,interval,reps,max_executions,inputs):
    start_time = time()
    
    random.seed(start_time)
    
    execution_interval = interval/max_executions
    execution_count = 0
    my_trials = []
    count = 0

    for rep in range(reps):
        for i in range(max_executions):
            start_time = time()

            # random.random -> fp from [0.0,1.0)
            # choose some random time between 0 and execution_interval seconds to wait before execution
            next_execution = random.random() * execution_interval
            
            my_trials += [None]

            # choose random code and exp from inputs 
            code, exp = inputs[random.randint(0,len(inputs)-1)]

            sleep(next_execution)
            
            execute_request(code, exp, my_trials, count)
            count += 1

            # wait until next execution interval
            if time() - start_time < execution_interval:
                sleep(execution_interval - (time() - start_time))

    trials[index] = my_trials



# ======================== SIMULATED STUDENT TESTS ========================
# Roughly simulate the access patterns for a student, i.e. for reps number of repitions of interval second tests,
# with max_executions number of executions of comp/run code in container.
# The code and expected output are 2-tuples pulled from the inputs [ (code,exp)^n ].
def run_student_test(service_name,test_name,student_count,interval,reps,max_executions,inputs):
    while not has_max_replicas(service_name):
        sleep(.1)

    trials = [None] * student_count
    threads = [None] * student_count

    for i in range(student_count):
        threads[i] = Thread(target=simulate_student,args=(trials,i,interval,reps,max_executions,inputs))
        threads[i].start()

    for i in range(student_count):
        threads[i].join((reps * interval) + 10)

    collected_trials = []

    for trial in trials:
        if trial:
            collected_trials += trial

    max_wait = interval/max_executions
    test = Test(test_name,"Student",student_count,interval,max_wait,collected_trials)

    if not len(collected_trials):
        print("WARNING: No test data collected")

    return test

def test_spawn_time(service_name,inputs):
    while not has_max_replicas(service_name):
        sleep(.1)

    command = ["docker", "service", "ls", "--filter", "name="+service_name, "--format", "{{.Replicas}}"]
    code, exp = inputs[2]
    has_containers = True
    thread_count = 0
    while has_containers:
        done_process = subprocess.run(command, 
                            stdout = subprocess.PIPE, 
                            stderr = subprocess.PIPE)
        out = done_process.stdout.decode("utf-8").split("/")
        err = done_process.stderr.decode("utf-8")

        count = int(out[0])
        total = int(out[1])

        if count > 0:
            if thread_count < total + 10:
                # INF CODE
                code, exp = inputs[2]
                thread = Thread(target=execute_request,args=(code,exp,[None],0,0))
                thread.start()
                thread_count += 1
        else:
            has_containers = False

    start_time = time()
    while not has_max_replicas(service_name):
        sleep(.01)
    end_time = time() - start_time

    return {"end_time":end_time, "total":total, "avg":end_time/total}

def main():
    service_name = "broncode_c_service"
    host = ''
    port = 4000
    flags = " -o3 \n" 

    bad_code = "int main(int argc,char** argv){error;return 0;}\n"
    bad_exp = "gcc -O3 -o code code.c\n" \
              "Something went wrong compiling your code:\n" \
              "code.c: In function 'main':\n" \
              "code.c:1:32: error: 'error' undeclared (first use in this function)\n" \
              " int main(int argc,char** argv){error;return 0;}\n" \
              "                                ^~~~~\n" \
              "code.c:1:32: note: each undeclared identifier is reported only once for each function it appears in\n"
        
    good_code = "int main(int argc,char** argv){printf(\"Hello!\\n\");return 0;}\n"
    good_exp  = "gcc -O3 -o code code.c\n" \
                "Executing program...\n" \
                "Your code successfully compiled and ran, here's the output:\n" \
                "./code\n" \
                "Hello!\n"

    inf_code =  "int main(int argc,char** argv){while(1);return 0;}\n"
    inf_exp  =  "Something went wrong running your code:\n" \
                "It took too long to execute, so we stopped it!\n"

    timeout_response = inf_exp

    inputs = [  (bad_code,bad_exp),
                (good_code,good_exp),
                (inf_code,inf_exp)  ]


    # ======================== SIMULATED STUDENT TESTS ========================

    tests = []
    # number of times to repeat the test over the interval 
    reps = 1
    # 60 second interval to execute num_executions
    interval = 30
    # number of executions to execute over each interval
    num_executions = 2

    # test with each one of these student counts
    student_counts = [1,5,10,20,30,40]
    # student_counts = [1,5,10,15,20,25,30]


    for i in range(len(student_counts)):
        test_name = "Simulated "+str(student_counts[i])+"-Student Test"
        test = run_student_test(service_name,test_name,student_counts[i],interval,reps,num_executions,inputs)
        tests += [test]
        print("Finished test: "+str(len(tests))+"/"+str(len(student_counts)))

    # process test results to ouput graph
    xdata, ydata, axis = visualizer.get_percent_success_vs_count(tests)
    
    log = "tests.log"
    for test in tests:
        visualizer.print_report(test)
        test.log_test(log)

    # output graph
    visualizer.scatter("Number of Students vs. % Successful Executions under 10 seconds For 30 Replicas",
                        xdata,
                        ydata,
                        axis,
                        "Student Count",
                        "% Successful executions with runtime < 10 sec",
                        ".png")



if __name__ == "__main__":
    main()
