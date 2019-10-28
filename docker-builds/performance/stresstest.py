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

# Hack: This is assigned in main, giving it global scope due to my own laziness
timeout_response = ""

# returns a Trial object corresponding to the results of the trial
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

    count = int(out[0])
    total = int(out[1])

    if err:
        return False

    return (count == total)

# ======================== NON THREADED TESTS ========================
# Every INTERVAL seconds, send code to the given service for compiling and running.
# Repeat the process REPS times.

def run_test(service_name,test_name,code,exp,total,interval,should_print=False):
    while not has_max_replicas(service_name):
        sleep(.1)

    trials = [None] * total

    for i in range(total):
        execute_request(code,exp,trials,i,interval)

    test = Test(test_name,"Single-Thread",total,interval,interval,trials)

    if should_print and trials:
        print_report(test)
    elif not trials:
        print("No test data collected")

    return test

# ======================== THREADED TESTS - Regular Interval ========================
# Start a thread every INTERVAL seconds that sends code to the given service for 
# compiling and running. Repeat the process REPS times.

# ======================== THREADED TESTS - Random Interval ========================
# Start a REPS threads and assign a random wait time within INTERVAL for the thread
# to begin execution, namely sending a code to the given service for compiling and running.

def run_threaded_test(service_name,test_name,code,exp,total,interval,is_random=False,should_print=False):
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
 
    if should_print and trials:
        print_report(test,is_random,seed)
    elif not trials:
        print("No test data collected")

    return test

def simulate_student(trials,index,time_limit,max_wait,inputs):
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
            sleep(.1)

    trials[index] = my_trials

# ======================== SIMULATED STUDENT TESTS ========================
# Roughly simulate the access patterns for a student, i.e. for time_limit seconds,
# wait a random time within max_wait, then execute_request to comp/run code in container.
# The code and expected output are 2-tuples pulled from the inputs [ (code,exp)^n ].
def run_student_test(service_name,test_name,student_count,time_limit,max_wait,inputs):
    while not has_max_replicas(service_name):
        sleep(.1)

    trials = [None] * student_count
    threads = [None] * student_count

    for i in range(student_count):
        threads[i] = Thread(target=simulate_student,args=(trials,i,time_limit,max_wait,inputs))
        threads[i].start()

    for i in range(student_count):
        threads[i].join(time_limit + 10)

    collected_trials = []

    for trial in trials:
        collected_trials += trial

    test = Test(test_name,"Student",student_count,time_limit,max_wait,collected_trials)

    if not len(collected_trials):
        print("WARNING: No test data collected")

    return test

def test_spawn_time(service_name,inputs):
    while not has_max_replicas(service_name):
        sleep(.1)

    command = ["docker", "service", "ls", "--filter", "name="+service_name, "--format", "{{.Replicas}}"]
    code, exp = inputs[2]
    has_containers = True
    while has_containers:
        done_process = subprocess.run(command, 
                            stdout = subprocess.PIPE, 
                            stderr = subprocess.PIPE)
        out = done_process.stdout.decode("utf-8").split("/")
        err = done_process.stderr.decode("utf-8")

        count = int(out[0])
        total = int(out[1])
        if count > 0:
            trials = [None] 
            execute_request(code,exp,trials,0)
        else:
            has_containers = False

    start_time = time()
    while not has_max_replicas(service_name):
        sleep(.01)
    end_time = time() - start_time

    return (end_time,total)

def main():
    service_name = "broncode_c_service"
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

    timeout_response = inf_exp

    inputs = [  (bad_code,bad_exp),
                (good_code,good_exp),
                (inf_code,inf_exp)  ]


    # ======================== SIMULATED STUDENT TESTS ========================

    tests = []
    time = 60
    reps = 3
    max_wait = 30
    

    max_tests = (6-1 + 7-3) * reps 
    for i in range(reps):
        # Values 5,10,15,25
        for j in range(1,6):
            tests += [run_student_test(service_name,"Simulated Student Test",j*5,time,max_wait,inputs)]
            print("Finished test: "+str(len(tests))+"/"+str(max_tests))
        # Values 30,40,50,60
        for j in range(3,7):
            tests += [run_student_test(service_name,"Simulated Student Test",j*10,time,max_wait,inputs)]
            print("Finished test: "+str(len(tests))+"/"+str(max_tests))

    visualizer.create_scat_plot("Simulated Student Test With 30 Docker Replicas",
                            tests,
                            "Number of Students",
                            "Percent of Executions Handled in < 8 Seconds")

    # print_report("Simulated Student Tests",test)

    # ======================== NON THREADED TESTS ========================

    # BAD CODE
    # code, exp = inputs[0]

    # run_tests(service_name,"Bad Code 5-interval",code,exp,reps,5)

    # ======================== THREADED TESTS - Regular Interval ========================

    # BAD CODE
    # code, exp = inputs[0]

    # run_threaded_tests(service_name,"Bad Code Threaded 5-interval",code,exp,reps,5)

    # ======================== THREADED TESTS - Random Interval ========================
    # BAD CODE
    # code, exp = inputs[0]

    # run_threaded_tests(service_name,"Bad Code Threaded Random 180-interval 60-Repitions",code,exp,reps,180,True)

if __name__ == "__main__":
    main()