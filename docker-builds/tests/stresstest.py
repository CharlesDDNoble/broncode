import subprocess
import math
import random
from threading import Thread, Timer
from time import time, sleep
from codehandler import CodeHandler

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

# returns tuple of total handler elapsed time and program runtime
def run_test(code, exp, is_threaded = False,tests=None,index=None,wait=0):
    sleep(wait)

    host = ''
    port = 4000
    flags = " -o3 \n" 

    start_time = time()
    
    handler = CodeHandler(host,port,code,flags)
    handler.run()
    
    elapsed_time = time() - start_time

    out = handler.log.replace('‘','\'').replace('’','\'')

    is_success = (out == exp)

    if is_threaded:
        tests[index] = (is_success,elapsed_time,handler.run_time)
        return

    return (is_success,elapsed_time,handler.run_time)


def is_passing(test):
    return test[0]

def is_failing(test):
    return not test[0]

def print_report(test_name,tests,is_random=False,seed=0):
    total = len(tests)
    sum_total_test_time = sum(e for s, e, r in tests)
    sum_total_run_time = sum(r for s, e, r in tests)

    passes = list(filter(is_passing,tests))
    pass_count = len(passes)
    sum_pass_test_time = sum(e for s, e, r in passes)
    sum_pass_run_time = sum(r for s, e, r in passes)

    fails = list(filter(is_failing,tests))
    fail_count = len(fails)
    sum_fails_test_time = sum(e for s, e, r in fails)
    sum_fails_run_time = sum(r for s, e, r in fails)

    print("===================================================")
    print(test_name+" Test Report:")

    if None in tests:
        print("WARNING: The tests list has an index with None!")
    
    if is_random:
        print("Random Seed used: "+str(seed))

    print("TOTALS")
    print("\tTotal tests run:               "+str(total))
    print("\tTotal test time:               "+str(sum_total_test_time))
    print("\tTotal connection and run time: "+str(sum_total_run_time))
    print("\tAvg. time of test:             "+str(sum_total_test_time/total))
    print("\tAvg. time to connect and run:  "+str(sum_total_run_time/total))

    if passes:
        print("PASSES")
        print("\tPasses/Total:                  "+str(pass_count)+"/"+str(total))
        print("\tTotal test time:               "+str(sum_pass_test_time))
        print("\tTotal connection and run time: "+str(sum_pass_run_time))
        print("\tAvg. time of test:             "+str(sum_pass_test_time/pass_count))
        print("\tAvg. time to connect and run:  "+str(sum_pass_run_time/pass_count))
    else:
        print("NO PASSING TESTS")

    if fails:
        print("FAILS")
        print("\tFails/Total:                   "+str(fail_count)+"/"+str(total))
        print("\tTotal test time:               "+str(sum_fails_test_time))
        print("\tTotal connection and run time: "+str(sum_fails_run_time))
        print("\tAvg. time to test:             "+str(sum_fails_test_time/fail_count))
        print("\tAvg. time to connect and run:  "+str(sum_fails_run_time/fail_count))
    else:
        print("NO FAILING TESTS")

    print("===================================================")

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

def run_tests(service_name,test_name,code,exp,total,interval):
    while not has_max_replicas(service_name):
        sleep(1)

    tests = []
    for i in range(total):
        test = run_test(code,exp)
        tests += [test]
        sleep(interval)

    print_report(test_name,tests)

def run_threaded_tests(service_name,test_name,code,exp,total,interval,is_random=False):
    while not has_max_replicas(service_name):
        sleep(1)

    seed = math.floor(time())
    random.seed(seed)

    tests = [None] * total
    threads = [None] * total

    for i in range(total):
        # assign a wait time based on the given interval for the thread to wait before execution
        if is_random:
            wait = random.random() * interval
        else:
            wait = interval * i

        thread = Thread(target=run_test,args=(code,exp,True,tests,i,wait))
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

    print_report(test_name,tests,is_random,seed)

def simulate_student(tests,index,time_limit,max_wait):
    start_time = time()
    
    random.seed(start_time)
    
    next_execution = random.random() * max_wait

    tests[index] = []

    while time() - start_time < time_limit:
        if next_execution <= 0:
            inp = math.floor(random.random() * len(inputs))
            code, exp = inputs[inp]
            tests[index] += [run_test(code, exp)]
            next_execution = 5 + random.random() * max_wait
        else:
            next_execution -= 1
            sleep(1)

def run_student_tests(service_name,test_name,total,time_limit,max_wait):
    while not has_max_replicas(service_name):
        sleep(1)

    tests = [None] * total
    threads = [None] * total

    for i in range(total):
        threads[i] = Thread(target=simulate_student,args=(tests,i,time_limit,max_wait))
        threads[i].start()

    for i in range(total):
        threads[i].join(time_limit + 10)

    collected_tests = []

    for i in range(total):
        collected_tests += tests[i]

    print_report(test_name,collected_tests)


def main():
    service_name = "broncode_service_c_web"
    reps = 60

    # ======================== NON THREADED TESTS ========================
    # Every INTERVAL seconds, send code to the given service for compiling and running.
    # Repeat the process REPS times.

    # BAD CODE
    # code, exp = inputs[0]

    # run_tests(service_name,"Bad Code 5-interval",code,exp,reps,5)

    # run_tests(service_name,"Bad Code 3-interval",code,exp,reps,3)

    # run_tests(service_name,"Bad Code 1-interval",code,exp,reps,1)

    # # GOOD CODE
    # code, exp = inputs[1]

    # run_tests(service_name,"Good Code 5-interval",code,exp,reps,5)

    # run_tests(service_name,"Good Code 3-interval",code,exp,reps,3)
    
    # run_tests(service_name,"Good Code 1-interval",code,exp,reps,1)

    # # INF CODE
    # code, exp = inputs[2]
    
    # run_tests(service_name,"Infinite Code 5-interval",code,exp,reps,5)

    # run_tests(service_name,"Infinite Code 3-interval",code,exp,reps,3)
    
    # run_tests(service_name,"Infinite Code 1-interval",code,exp,reps,1)

    # ======================== THREADED TESTS - Regular Interval ========================
    # Start a thread every INTERVAL seconds that sends code to the given service for 
    # compiling and running. Repeat the process REPS times.

    # BAD CODE
    # code, exp = inputs[0]

    # run_threaded_tests(service_name,"Bad Code Threaded 5-interval",code,exp,reps,5)

    # run_threaded_tests(service_name,"Bad Code Threaded 3-interval",code,exp,reps,3)

    # run_threaded_tests(service_name,"Bad Code Threaded 1-interval",code,exp,reps,1)

    # # GOOD CODE
    # code, exp = inputs[1]

    # run_threaded_tests(service_name,"Good Code Threaded 5-interval",code,exp,reps,5)

    # run_threaded_tests(service_name,"Good Code Threaded 3-interval",code,exp,reps,3)

    # run_threaded_tests(service_name,"Good Code Threaded 1-interval",code,exp,reps,1)

    # # INF CODE
    # code, exp = inputs[0]

    # run_threaded_tests(service_name,"Infinite Code Threaded 5-interval",code,exp,reps,5)

    # run_threaded_tests(service_name,"Infinite Code Threaded 3-interval",code,exp,reps,3)

    # run_threaded_tests(service_name,"Infinite Code Threaded 1-interval",code,exp,reps,1)

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

    run_student_tests(service_name,"Simulated Student Test 60-limit",15,60,20)


if __name__ == "__main__":
    main()